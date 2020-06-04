import unittest

from main import (validate_password, validate_email)


class TestValidatePassword(unittest.TestCase):
    def test_password_shorter_than_eight_symbols_returns_false(self):
        password = '1234567'
        message = 'password must be min 8 characters long'

        with self.assertRaises(ValueError, msg=message):
            validate_password(password)

    def test_long_password_with_no_capital_letters_returns_false(self):
        password = '12345678'
        message = 'password must contain a capital letter'

        with self.assertRaises(ValueError, msg=message):
            validate_password(password)

    def test_long_password_with_capital_letter_without_special_symbols(self):
        password = '12345678A'
        message = 'password must contain a special symbol'

        with self.assertRaises(ValueError, msg=message):
            validate_password(password)

    def test_password_with_eigh_symbols_with_one_capital_and_one_special(self):
        password = 'A12$4567'

        validate_password(password)


class TestValidateEmail(unittest.TestCase):
    def test_email_without_at_symbol_returns_false(self):
        email = 'example.example.com'

        with self.assertRaises(ValueError):
            validate_email(email)

    def test_email_with_at_symbol_but_unvalid_returns_false(self):
        email1 = 'example@example@com'
        email2 = 'example@'
        # email3 = '@example.com'

        with self.assertRaises(ValueError):
            validate_email(email1)

        with self.assertRaises(ValueError):
            validate_email(email2)

        # with self.assertRaises(ValueError):
        #     UserModel.validate_email(email3)

    def test_with_correct_input_returns_true(self):
        email = 'name@example.com'

        validate_email(email)


if __name__ == '__main__':
    unittest.main()
