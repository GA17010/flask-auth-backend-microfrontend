from marshmallow import Schema, fields, validate, ValidationError, post_load

def validate_has_uppercase(password):
    if not any(c.isupper() for c in password):
        raise ValidationError('The password must contain at least one capital letter.')

def validate_has_special_char(password):
    special_chars = "@#$%&"
    if not any(c in special_chars for c in password):
        raise ValidationError(f'The password must contain at least one of the following characters: {special_chars}')

class UserSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    company = fields.String(allow_none=True, validate=validate.Length(max=100))
    password = fields.String(required=True, validate=[validate.Length(min=8, max=50), validate_has_uppercase, validate_has_special_char], load_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=8))

class RegistrationSchema(UserSchema):
    confirm_password = fields.Str(required=True, load_only=True)
    
    @post_load
    def validate_passwords_match(self, data, **kwargs):
        if data["password"] != data["confirm_password"]:
            raise ValidationError({"confirm_password": "Passwords must match."})
        return data

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=8))

class ResetPasswordSchema(Schema):
    otp = fields.String(required=True, validate=validate.Length(equal=6))
    email = fields.Email(required=True, validate=validate.Length(min=8))
    password = fields.String(required=True, validate=[validate.Length(min=8, max=50), validate_has_uppercase, validate_has_special_char], load_only=True)