import unittest
from unittest.mock import patch

from fastapi import HTTPException

from src import app as app_module


class SignupCapacityTests(unittest.TestCase):
    def test_signup_takes_last_available_spot(self):
        activity = {
            "max_participants": 2,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(app_module.activities, {"Test Activity": activity}):
            result = app_module.signup_for_activity(
                "Test Activity", "new@mergington.edu"
            )

        self.assertEqual(
            result,
            {"message": "Signed up new@mergington.edu for Test Activity"},
        )
        self.assertEqual(
            activity["participants"],
            ["existing@mergington.edu", "new@mergington.edu"],
        )

    def test_signup_rejects_full_activity(self):
        activity = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(app_module.activities, {"Test Activity": activity}):
            with self.assertRaises(HTTPException) as raised:
                app_module.signup_for_activity(
                    "Test Activity", "new@mergington.edu"
                )

        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(raised.exception.detail, "Activity is full")
        self.assertEqual(activity["participants"], ["existing@mergington.edu"])

    def test_duplicate_signup_error_is_unchanged(self):
        activity = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

        with patch.dict(app_module.activities, {"Test Activity": activity}):
            with self.assertRaises(HTTPException) as raised:
                app_module.signup_for_activity(
                    "Test Activity", "existing@mergington.edu"
                )

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.detail, "Student is already signed up")


if __name__ == "__main__":
    unittest.main()
