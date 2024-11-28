from PIL import Image

quadrado_largura, quadrado_altura = 768, 128

sprite = Image.open("/home/lucas-lima/Documentos/A2-LP/shattered/assets/Knight/Dead.png")
sprite_largura, sprite_altura = sprite.size

offset_x = 32
offset_y = 0

quadrado = Image.new("RGBA", (quadrado_largura, quadrado_altura), (0, 0, 0, 0))

quadrado.paste(sprite, (offset_x, offset_y), sprite)

quadrado.save("/home/lucas-lima/Documentos/A2-LP/shattered/assets/Knight/Dead1.png")
