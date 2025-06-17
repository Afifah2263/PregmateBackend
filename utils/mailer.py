import smtplib
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash
from models.datauser_model import User

OTP_EXPIRE_MINUTES = 10

def send_email(to_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "rizkiekamulyani123@gmail.com"        # Ganti sesuai email kamu
    smtp_password = "ykfa bxvy ihly thqm"     # Ganti sesuai password/app password

    msg = MIMEText(message)
    msg['Reply-To'] = smtp_user
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [to_email], msg.as_string())
        server.quit()
        print("Berhasil mengirim email.")
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

def request_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email harus diisi"}), 400

    user = User.find_by_email(email)
    if not user:
        return jsonify({"error": "Email tidak ditemukan"}), 404

    otp = f"{random.randint(100000, 999999)}"

    otp_data = {
        "otp": otp,
        "otp_expired_at": datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    }
    User.db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": otp_data}
    )

    subject = "Kode OTP untuk Reset Password"
    message = f"Kode OTP Anda adalah: {otp}. Kode ini berlaku selama {OTP_EXPIRE_MINUTES} menit."
    if send_email(email, subject, message):
        return jsonify({"message": "OTP berhasil dikirim ke email"}), 200
    else:
        return jsonify({"error": "Gagal mengirim email"}), 500

def reset_password():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')

    if not email or not otp or not new_password:
        return jsonify({"error": "Email, OTP, dan password baru harus diisi"}), 400

    user = User.find_by_email(email)
    if not user:
        return jsonify({"error": "Email tidak ditemukan"}), 404

    stored_otp = user.get('otp')
    otp_expired_at = user.get('otp_expired_at')

    if stored_otp != otp:
        return jsonify({"error": "OTP salah"}), 400

    if not otp_expired_at or datetime.utcnow() > otp_expired_at:
        return jsonify({"error": "OTP sudah kadaluwarsa"}), 400

    # Gantilah hash password menggunakan werkzeug (biar konsisten dengan login_user)
    hashed_password = generate_password_hash(new_password)

    User.db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": {
            "password": hashed_password,
            "otp": None,
            "otp_expired_at": None
        }}
    )

    return jsonify({"message": "Password berhasil direset"}), 200,