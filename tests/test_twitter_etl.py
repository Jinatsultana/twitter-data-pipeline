import unittest

import pandas as pd

from scripts.twitter_etl import transform_data, validate_data


class TestTwitterETL(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            "author": ["user1", "user2", "user1"],
            "content": ["Hello", "Data Engineering", "Hello again"],
            "country": ["India", "India", "India"],
            "date_time": [
                "2026-01-01 10:00:00",
                "2026-01-02 11:00:00",
                "2026-01-03 12:00:00"
            ],
            "id": [101, 102, 101],
            "language": ["en", "en", "en"],
            "number_of_likes": [10, 20, 15],
            "number_of_shares": [2, 5, 3],
            "latitude": [None, None, None],
            "longitude": [None, None, None]
        })

    def test_transform_removes_duplicate_ids(self):
        result = transform_data(self.sample_data)

        self.assertEqual(len(result), 2)

        self.assertEqual(
            result["id"].duplicated().sum(),
            0
        )

    def test_transform_renames_columns(self):
        result = transform_data(self.sample_data)

        expected_columns = [
            "user",
            "text",
            "country",
            "created_at",
            "id",
            "language",
            "like_count",
            "share_count"
        ]

        self.assertEqual(
            list(result.columns),
            expected_columns
        )

    def test_validate_data_passes(self):
        result = transform_data(self.sample_data)

        validate_data(result)

    def test_validate_data_rejects_duplicate_ids(self):
        result = transform_data(self.sample_data)

        result.loc[1, "id"] = result.loc[0, "id"]

        with self.assertRaises(ValueError):
            validate_data(result)


if __name__ == "__main__":
    unittest.main()