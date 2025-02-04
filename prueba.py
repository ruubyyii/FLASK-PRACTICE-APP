from werkzeug.security import check_password_hash

hash_guardado = "scrypt:32768:8:1$6YfVrLLwxRGfdHsg$cca3e5ed20b7566441cd85292be0a7cd29519eb4269374ad304ed790c8366c814e60c30bfce92fa3d83997fd645379140b6e46debff67c38e25792355ccbebff"
password_ingresada = "abbu"  # Cambia esto por la contraseña real que usaste

if check_password_hash(hash_guardado, password_ingresada):
    print("✅ Contraseña correcta")
else:
    print("❌ Contraseña incorrecta")
