"""Basic validation suite for AI02 prototype (run: py -m unittest discover -s tests)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import BY_ID, SCHEMES, VERIFIED_DATE, app, build_answer, detect_scheme, detect_topic, search_schemes, sources_are_official  # noqa: E402


class SchemeDataTests(unittest.TestCase):
    def test_five_schemes_loaded(self):
        self.assertEqual(len(SCHEMES), 5)

    def test_every_scheme_has_bilingual_fields_sources_and_verification(self):
        required = [
            "name_ta", "name_en", "who_ta", "who_en", "benefit_ta", "benefit_en",
            "eligibility_ta", "eligibility_en", "documents_ta", "documents_en",
            "apply_steps_ta", "apply_steps_en", "caveat_ta", "caveat_en",
            "apply_url", "official_sources", "last_verified",
        ]
        for scheme in SCHEMES:
            with self.subTest(scheme=scheme["id"]):
                for key in required:
                    self.assertTrue(scheme.get(key), f"missing {key}")
                self.assertEqual(scheme["last_verified"], VERIFIED_DATE)
                self.assertGreaterEqual(len(scheme["official_sources"]), 1)

    def test_all_links_point_to_official_domains(self):
        self.assertTrue(sources_are_official())


class LogicTests(unittest.TestCase):
    def test_scheme_detection_tamil_and_english(self):
        self.assertEqual(detect_scheme("கலைஞர் மகளிர் உரிமைத் திட்டம்"), "kmut")
        self.assertEqual(detect_scheme("PM Kisan eligibility"), "pmkisan")
        self.assertEqual(detect_scheme("SHG கடன்"), "daynrlm")
        self.assertEqual(detect_scheme("mudra loan for my shop"), "pmmy")
        self.assertEqual(detect_scheme("சுகன்யா சம்ரித்தி ஆவணங்கள்"), "ssy")
        self.assertIsNone(detect_scheme("இந்தியாவின் தலைநகரம் எது?"))

    def test_topic_detection(self):
        self.assertEqual(detect_topic("கலைஞர் திட்டத்திற்கு என்ன ஆவணங்கள் தேவை?"), "documents")
        self.assertEqual(detect_topic("Who is not eligible for PM Kisan?"), "exclusions")
        self.assertEqual(detect_topic("How do I apply for Mudra?"), "apply")
        self.assertEqual(detect_topic("PM Kisan"), "overview")

    def test_search(self):
        self.assertEqual(search_schemes("கலைஞர்")[0]["id"], "kmut")
        self.assertEqual(search_schemes("sukanya")[0]["id"], "ssy")
        self.assertEqual(search_schemes("farmer")[0]["id"], "pmkisan")
        self.assertEqual(len(search_schemes("xyz-not-a-scheme")), 0)

    def test_answer_contains_caveat_and_source(self):
        answer = build_answer("கலைஞர் திட்டத்திற்கு தகுதி என்ன?", "ta")
        self.assertEqual(answer["scheme_id"], "kmut")
        self.assertIn("தகுதி", answer["title"])
        self.assertTrue(answer["bullets"])
        self.assertIn("இறுதி தகுதியை", answer["caveat"])
        self.assertTrue(answer["sources"][0].startswith("KMUT"))

    def test_unknown_query_does_not_invent_facts(self):
        answer = build_answer("ரசியல் கட்சி பற்றி கூறு", "en")
        self.assertIsNone(answer["scheme_id"])
        self.assertEqual(answer["bullets"], [])
        self.assertIn("No scheme matched", answer["text"])


class WebTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_renders_tamil_by_default(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("அரசு திட்டங்களை எளிய தமிழில் புரிந்து கொள்ளுங்கள்", html)
        self.assertIn("கலைஞர் மகளிர் உரிமைத் திட்டம்", html)

    def test_language_switch(self):
        html = self.client.get("/?lang=en").get_data(as_text=True)
        self.assertIn("Government schemes, explained simply", html)
        self.assertIn("Kalaignar Magalir Urimai Thogai", html)

    def test_search_filters_cards(self):
        html = self.client.get("/?q=mudra").get_data(as_text=True)
        self.assertIn("பிரதமர் முத்ரா யோஜனா", html)
        self.assertNotIn("சுகன்யா சம்ரித்தி யோஜனா", html)

    def test_detail_page_has_sources_and_no_input_fields(self):
        html = self.client.get("/scheme/kmut?lang=en").get_data(as_text=True)
        self.assertEqual(self.client.get("/scheme/kmut").status_code, 200)
        self.assertIn("kmut.tn.gov.in", html)
        self.assertIn("2026-11-18", html)
        self.assertNotIn("<input", html)

    def test_ask_endpoint_tamil_and_english(self):
        ta = self.client.post("/ask", json={"q": "முத்ரா கடனுக்கு ஆவணங்கள் என்ன?", "lang": "ta"})
        self.assertEqual(ta.status_code, 200)
        data = ta.get_json()
        self.assertEqual(data["scheme_id"], "pmmy")
        self.assertIn("ஆவண", data["title"])

        en = self.client.post("/ask", json={"q": "Sukanya Samriddhi documents", "lang": "en"})
        self.assertEqual(en.get_json()["scheme_id"], "ssy")
        self.assertIn("Documents", en.get_json()["title"])

    def test_api_and_health(self):
        self.assertEqual(self.client.get("/healthz").get_data(as_text=True), "ok")
        data = self.client.get("/api/schemes?lang=en").get_json()
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["verified"], VERIFIED_DATE)

    def test_unknown_scheme_id_is_404(self):
        self.assertEqual(self.client.get("/scheme/does-not-exist").status_code, 404)

    def test_no_personal_data_collection_in_forms(self):
        html = self.client.get("/").get_data(as_text=True)
        inputs = html.lower().count("<input")
        self.assertEqual(inputs, 3, "expected only: hidden lang, search box, question box")
        for sensitive in ["aadhaar_number", "account_number", " ration_no", "type=\"password\""]:
            self.assertNotIn(sensitive, html.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
