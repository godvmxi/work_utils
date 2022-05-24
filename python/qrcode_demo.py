__author__ = 'bluebird'
def generate_qrcode():
    import qrcode
    q=qrcode.main.QRCode()
    q.add_data("http://www.baidu.com")
    q.make()
    m=q.make_image()
    m.save('/home/bluebird/char.png')
def read_qrcode():
    import zbar,Image
    scanner = zbar.ImageScanner()
    scanner.parse_config("enable")
    pil = Image.open("/home/bluebird/char.png").convert('L')
    width, height = pil.size
    raw = pil.tostring()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    data = ''
    for symbol in image:
        data+=symbol.data
    del(image)
    return data



print read_qrcode()