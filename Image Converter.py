from PIL import Image                      

import rawpy as RAW                        

import tkinter as tk                       
from tkinter import ttk, filedialog     

from pathlib import Path





def converter_imagens(pasta_original, formato_desejado, log_widget):

    pasta_original = Path(pasta_original)   

    pasta_saida = pasta_original / f"Fotografias{formato_desejado.lower()}"
    pasta_saida.mkdir(exist_ok = True)  


    formatos_comuns = ['.jpg', '.jpeg', '.png', '.tiff']
    formatos_raw = ['.cr3', '.nef', '.arw', '.dng']


    for ficheiro in pasta_original.iterdir():
        if not ficheiro.is_file():
            continue

        extensão = ficheiro.suffix.lower()

       
        if extensão in formatos_comuns:
            
    
                
                imagem = Image.open(ficheiro)
                
                if formato_desejado.upper() == "JPEG" and imagem.mode in ("RGBA", "P"):
                    imagem = imagem.convert("RGB")
                
                elif formato_desejado.upper() == "PNG" and imagem.mode not in ("RGBA", "RGB"):
                    imagem = imagem.convert("RGBA")
               
                elif formato_desejado.upper() == "TIFF" and imagem.mode not in ("RGBA", "RGB"):
                    imagem = imagem.convert("RGBA")

                caminho_imagem = pasta_saida / f"{ficheiro.stem}.{formato_desejado.lower()}"

                imagem.save(caminho_imagem, format = formato_desejado, quality = 95)

                log_widget.insert(tk.END, f"Conversão Concluída - {ficheiro.name} → {caminho_imagem.name}\n")

                imagem.close()

          
        

        elif extensão in formatos_raw:

            

                with RAW.imread(str(ficheiro)) as raw:
                    RGB = raw.postprocess(
                        use_camera_wb = True,   
                        output_bps = 8,        
                        no_auto_bright = False,  
                        gamma = (2.2 , 4.5),        
                        output_color = RAW.ColorSpace.sRGB 
                    )


                    imagem_raw = Image.fromarray(RGB)

                   
                    if formato_desejado.upper() == "JPEG" and imagem_raw.mode in ("RGBA", "P"):
                        imagem_raw = imagem_raw.convert("RGB")

                    elif formato_desejado.upper() == "PNG" and imagem_raw.mode not in ("RGBA", "RGB"):
                        imagem_raw = imagem_raw.convert("RGBA")

                    elif formato_desejado.upper() == "TIFF" and imagem_raw.mode not in ("RGBA", "RGB"):
                        imagem_raw = imagem_raw.convert("RGBA")

                    caminho_imagem_raw = pasta_saida / f"{ficheiro.stem}.{formato_desejado.lower()}"

                    imagem_raw.save(caminho_imagem_raw, format = formato_desejado, quality = 95)

                    log_widget.insert(tk.END, f"Conversão RAW Concluída - {ficheiro.name} → {caminho_imagem_raw.name}\n")

                    imagem_raw.close()





def selecionar_pasta():

    pasta = filedialog.askdirectory()
    if pasta:
        entrada_var.set(pasta)



janela = tk.Tk()
janela.title("Conversor de Imagens - Eliezer Carvalho")
janela.geometry("1200x1200")
#janela.iconbitmap(r"C:\Users\eliez\Desktop\upload_document_content_marketing_seo_digital_guest_post_submission_icon_267785.ico")
janela.config(bg = "#101820")


entrada_var = tk.StringVar()
formato_var = tk.StringVar(value = "PNG")


botão_selecionar_pasta = tk.Button(janela, text = "SELECIONAR PASTA", command = selecionar_pasta, bg = "#101820", fg = "#FEE715",  relief  = "flat").pack(pady = 20)
linha_de_entrada = tk.Entry(janela, textvariable = entrada_var, width = 100).pack(pady = (0, 15))



formato_saída = tk.Label(janela, text = "FORMATO DE SAÍDA DESEJADO:", bg = "#101820", fg = "#FEE715").pack(pady = (25, 15))
opcoes_conversão = ttk.Combobox(janela, textvariable = formato_var, values = ["PNG", "JPEG", "TIFF"], state = "readonly").pack(pady = (0, 15))


botão_conversão = tk.Button(janela, text = "CONVERTER FICHEIRO!", bg = "#101820", fg = "#FEE715", relief = "flat", command = lambda: converter_imagens(entrada_var.get(), formato_var.get(), log_text)).pack(pady = (25, 15))


log_text = tk.Text(janela, height = 15, width = 70)
log_text.pack(pady = (0, 15))

janela.mainloop()