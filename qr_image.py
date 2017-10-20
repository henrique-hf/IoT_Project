import qrcode

# Ho aggiunto in DatabaseManager questa funzione, qrCodeGenerator(self, packetID).
# bisognerebbe riuscire a fornirgli il packetID, per averli sempre abbinati
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("If you are reading this code, I've been successful ")
qr.make(fit=True)

img = qr.make_image()
img.show()
img = qr.make_image()
packetID = "abc123"
name = 'QRcodeP_' + packetID + '.png'
img.save(name)
