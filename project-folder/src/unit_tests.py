"""Unit tests for weather analysis helpers."""

import unittest

import functions


class WeatherFunctionTests(unittest.TestCase):
    def test_get_data_whole_skips_header(self):
        seq = (
            ("date", "value"),
            ("2014-1-1", 10),
            ("2014-1-2", 20),
            ("2014-1-3", 30),
        )
        self.assertEqual(functions.get_data_whole(seq, 1), (10, 20, 30))

    def test_get_data_date_handles_single_and_double_digit_months(self):
        seq = (
            ("date", "value"),
            ("2014-1-1", 1),
            ("2014-10-1", 2),
            ("2014-01-15", 3),
            ("2015-1-1", 4),
        )
        self.assertEqual(functions.get_data_date(seq, 1, 2014, 1), (1, 3))

    def test_highest_in_sequence_checks_first_item(self):
        seq = (99, 5, 6, 7)
        self.assertEqual(functions.highest_in_sequence(seq), (99, 0))

    def test_average_change_uses_point_intervals(self):
        seq = (2, 4, 8, 14)
        self.assertAlmostEqual(functions.average_change(seq), 4.0)

    def test_statistics_whole_with_threshold(self):
        seq = (1, 4, 7, 10)
        stats = functions.statistics_whole(seq, threshold=5)
        self.assertAlmostEqual(stats["average"], 5.5)
        self.assertEqual(stats["highest_value"], 10)
        self.assertEqual(stats["highest_index"], 3)
        self.assertEqual(stats["count_at_or_above_threshold"], 2)
        self.assertEqual(stats["count_at_or_below_threshold"], 2)

    def test_statistics_whole_rejects_empty_sequence(self):
        with self.assertRaises(ValueError):
            functions.statistics_whole(())

    def test_station_display_mapping(self):
        display_name = functions.station_code_to_display("KCLT")
        self.assertEqual(display_name, "Charlotte, North Carolina")
        self.assertIn(display_name, functions.get_station_display_options())

    def test_year_range_from_dataset(self):
        self.assertEqual(functions.get_valid_year_range(), (2014, 2015))

    def test_available_months_for_los_angeles_2014(self):
        months = functions.get_available_months_for_year("Los Angeles, California", 2014)
        self.assertEqual(months, (7, 8, 9, 10, 11, 12))

    def test_detect_anomalies_flags_outlier(self):
        values = (10, 10, 10, 100, 10)
        anomalies, mean_value, std_dev = functions.detect_anomalies(values, z_threshold=1.5)

        self.assertGreater(std_dev, 0)
        self.assertAlmostEqual(mean_value, 28.0)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["index"], 3)

    def test_detect_anomalies_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            functions.detect_anomalies((1, 2, 3), z_threshold=0)

    def test_calculate_similarity_metrics_identical_series(self):
        metrics = functions.calculate_similarity_metrics((1, 2, 3), (1, 2, 3))
        self.assertAlmostEqual(metrics["rmse"], 0.0)
        self.assertAlmostEqual(metrics["mae"], 0.0)
        self.assertAlmostEqual(metrics["correlation"], 1.0)

    def test_align_series_by_date(self):
        aligned_dates, aligned_a, aligned_b = functions._align_series_by_date(
            ("d1", "d2", "d3"),
            (1, 2, 3),
            ("d2", "d3", "d4"),
            (20, 30, 40),
        )
        self.assertEqual(aligned_dates, ("d2", "d3"))
        self.assertEqual(aligned_a, (2, 3))
        self.assertEqual(aligned_b, (20, 30))

    def test_analyze_city_similarity_returns_top_n(self):
        result = functions.analyze_city_similarity(
            reference_station="Charlotte, North Carolina",
            column="Mean temperature",
            use_month=False,
            top_n=3,
            show_plot=False,
        )

        self.assertEqual(result["reference_city"], "Charlotte, North Carolina")
        self.assertEqual(len(result["ranked_cities"]), 3)
        self.assertNotIn(
            "Charlotte, North Carolina",
            [item["city"] for item in result["ranked_cities"]],
        )


if __name__ == "__main__":
    unittest.main()
