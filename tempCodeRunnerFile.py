img_url = ' '.join([str(elem) for elem in crypto_img])
        # res = requests.get(img_url, stream = True)
        # try:
        #     if res.status_code == 200:
        #         with open(crypto_name,'wb') as f:
        #             shutil.copyfileobj(res.raw, f) 
        #         print('Image sucessfully Downloaded: ', crypto_name)
        #     else:
        #         pass
        # except Exception:
        