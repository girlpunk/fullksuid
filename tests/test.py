import unittest
import datetime


class MyTestCase(unittest.TestCase):
    def test_decode(self):
        import fullksuid

        instance = fullksuid.Id.parse("example_000000C8BhNf4i3xUDfqSfNblvptQ")
        self.assertEqual(instance.resource, "example")
        self.assertEqual(instance.environment, "prod")
        self.assertEqual(instance.timestamp, datetime.datetime(2021, 4, 29, 10, 45, 22))
        self.assertEqual(instance.instance.scheme, fullksuid.Schemes.MAC_AND_PID)
        self.assertEqual(instance.instance.identifier.hex(), "1e00a23e5390"+int(20781).to_bytes(2, "big").hex())
        self.assertEqual(instance.sequenceId, 0)

    def test_encode(self):
        import fullksuid

        print(fullksuid.generate("test"))
        self.assertIsNotNone(fullksuid.generate("test"))

    def test_both(self):
        import fullksuid

        instance = fullksuid.generate("test")
        self.assertIsNotNone(instance)

        parsed = fullksuid.Id.parse(instance.__str__())

        print(f"ID: {parsed.__str__():>36}")
        print(f"Resource: {parsed.resource:>30}")
        print(f"Environment: {parsed.environment:>27}")
        print(f"Timestamp: {parsed.timestamp.__str__():>29}")
        print(f"Instance: {parsed.instance.__str__():>18}")
        print(f"Sequence ID: {parsed.sequenceId:>27}")


if __name__ == '__main__':
    unittest.main()
