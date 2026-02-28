def generate_password_reset_html(reset_link: str, project_name: str) -> str:
    """
    Generate HTML for password reset email.
    """
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Şifre Sıfırlama</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #eeeeee;
        }}
        .content {{
            padding: 20px 0;
            line-height: 1.6;
        }}
        .button-wrapper {{
            text-align: center;
            margin: 30px 0;
        }}
        .button {{
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: #888888;
            padding-top: 20px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0;">{project_name}</h2>
        </div>
        <div class="content">
            <p>Merhaba,</p>
            <p>Hesabınız için şifre sıfırlama talebinde bulundunuz. Şifrenizi yenilemek için aşağıdaki butona tıklayabilirsiniz:</p>
            <div class="button-wrapper">
                <a href="{reset_link}" class="button">Şifremi Yenile</a>
            </div>
            <p>Eğer bu talebi siz yapmadıysanız, bu e-postayı güvenle görmezden gelebilirsiniz.</p>
            <p>Bu bağlantı kısa bir süreliğine geçerlidir.</p>
        </div>
        <div class="footer">
            <p>&copy; {project_name}. Tüm hakları saklıdır.</p>
        </div>
    </div>
</body>
</html>"""


def generate_email_verification_html(verify_link: str, project_name: str) -> str:
    """
    Generate HTML for email verification.
    """
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>E-posta Doğrulama</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #eeeeee;
        }}
        .content {{
            padding: 20px 0;
            line-height: 1.6;
        }}
        .button-wrapper {{
            text-align: center;
            margin: 30px 0;
        }}
        .button {{
            background-color: #28a745;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: #888888;
            padding-top: 20px;
            border-top: 1px solid #eeeeee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin: 0;">{project_name}</h2>
        </div>
        <div class="content">
            <p>Merhaba,</p>
            <p>Aramıza hoş geldiniz! Kayıt işleminizi tamamlamak ve e-posta adresinizi doğrulamak için lütfen aşağıdaki butona tıklayın:</p>
            <div class="button-wrapper">
                <a href="{verify_link}" class="button">E-posta Adresimi Doğrula</a>
            </div>
            <p>Eğer bu hesabı siz oluşturmadıysanız, bu e-postayı görmezden gelebilirsiniz.</p>
        </div>
        <div class="footer">
            <p>&copy; {project_name}. Tüm hakları saklıdır.</p>
        </div>
    </div>
</body>
</html>"""
