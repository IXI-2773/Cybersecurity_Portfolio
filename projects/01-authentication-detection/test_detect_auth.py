import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from detect_auth import find_suspicious_logins, parse_timestamp, read_events

BASE = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)


def event(minute, kind, username="alice", source_ip="192.0.2.15"):
    return {
        "dt": BASE + timedelta(minutes=minute),
        "username": username,
        "source_ip": source_ip,
        "host": "LAB-DC1",
        "event_type": kind,
    }


class DetectionTests(unittest.TestCase):
    def test_synthetic_fixture_has_one_finding(self):
        source = Path(__file__).parent / "auth_events.csv"
        results = find_suspicious_logins(read_events(source))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["username"], "alice")
        self.assertEqual(results[0]["failure_count_in_window"], 6)

    def test_below_threshold(self):
        self.assertEqual(find_suspicious_logins(
            [event(i, "login_failure") for i in range(4)] +
            [event(4, "login_success")]), [])

    def test_expired_window(self):
        self.assertEqual(find_suspicious_logins(
            [event(i, "login_failure") for i in range(5)] +
            [event(20, "login_success")]), [])

    def test_user_and_ip_isolation(self):
        events = [event(i, "login_failure") for i in range(5)]
        events.extend([event(5, "login_success", "bob"),
                       event(6, "login_success", "alice", "198.51.100.44")])
        self.assertEqual(find_suspicious_logins(events), [])

    def test_out_of_order(self):
        events = [event(6, "login_success")] + [
            event(i, "login_failure") for i in range(5)]
        self.assertEqual(len(find_suspicious_logins(events)), 1)

    def test_inclusive_window_boundary(self):
        events = [event(i, "login_failure") for i in range(5)]
        events.append(event(10, "login_success"))
        self.assertEqual(len(find_suspicious_logins(events)), 1)

    def test_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            parse_timestamp("not-a-time")

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            find_suspicious_logins([], threshold=0)

    def test_suppress_consecutive_successes(self):
        events = [event(i, "login_failure") for i in range(5)]
        events.extend([event(5, "login_success"), event(6, "login_success")])
        self.assertEqual(len(find_suspicious_logins(events)), 1)


if __name__ == "__main__":
    unittest.main()
