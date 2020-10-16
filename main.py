#Desenvolvido por:
#Levy Barbosa e Gustavo Lopes
#Fundamentos da Programação 2020.1
#Ciência da Computação
#IFCE Maracanaú

import tkinter as tk
import math
import json
import tkinter.messagebox

currentPage=1

def readJson():
    global numberPages,dataRaw,produtos,dataLenght
    try:
        with open('produtos.json', 'r', encoding="utf-8") as json_file:
            dataRaw = json.load(json_file)
            data=dataRaw.copy()
            dataLenght=len(dataRaw)
            if (dataLenght==0):
                toComplete=20
            else:
                toComplete=(math.ceil(dataLenght/20)*20)-dataLenght
            for i in range(toComplete):
                data.append({'code': None, 'product': None , 'price': None})
            numberPages=int(len(data)/20)
            return data
    except:
        writeToJson([])
        return readJson()

def writeToJson(savedata):
    with open('produtos.json', 'w', encoding="utf-8") as outfile:
        json.dump(savedata, outfile,indent=4)

def nextPage():
    global currentPage
    currentPage=int(currentPage)
    if(currentPage<numberPages):
        currentPage+=1
        updatePageEntry()

def previousPage():
    global currentPage
    currentPage=int(currentPage)
    if(currentPage>1):
        currentPage-=1
        updatePageEntry()

def setPage(event=None):
    global currentPage,ent_currentPage
    if(type(event)==tk.Event):
        labelValue=ent_currentPage.get()
    else:
        labelValue=numberPages
    if(labelValue!=''):
        currentPage=int(labelValue)
    updatePageEntry()

def updatePageEntry():
    ent_currentPage.delete(0,tk.END)
    ent_currentPage.insert(0,str(currentPage))
    updateTable(currentPage)

def checkPageInput(entInput):
    if(entInput==''):
        return True
    try:
        entInput=int(entInput)
        if(entInput>0 and entInput<=numberPages):
            return True
        else:
            return False
    except:
        return False

def checkPriceInput(entInput):
    entInput=entInput.replace(',','.')
    if(entInput==''):
        return True
    try:
        entInput=float(entInput)
        if(entInput>=0):
            return True
        else:
            return False
    except:
        return False

def codeValidation(entInput):
    try:
        entInput=int(entInput)
    except:
        if entInput!='':
            return False
    return True


def renderTable(page):
    page=int(page)
    columns=['Código','Produto','Preço','']
    for i in range(len(columns)):
        frm_columnHeader=tk.Frame(
            master=frm_table
        )
        frm_columnHeader.grid(row=0, column=i,sticky='nesw',padx=1,pady=1)
        label = tk.Label(master=frm_columnHeader,text=columns[i])
        label.pack()

    rowCount=1
    for i in range(20):

        frm_cod=tk.Frame(master=frm_table, bg="white")  
        frm_cod.grid(row=rowCount, column=0, sticky='nesw', padx=1, pady=1) 
       
        frm_prod=tk.Frame(master=frm_table, bg="white")
        frm_prod.grid(row=rowCount, column=1, sticky='nesw', padx=1, pady=1) 
      
        frm_price=tk.Frame(master=frm_table, bg="white")
        frm_price.grid(row=rowCount, column=2, sticky='nesw', padx=1, pady=1)

        frm_checkbox=tk.Frame(master=frm_table, bg="white")
        frm_checkbox.grid(row=rowCount, column=3, sticky='nesw', padx=1, pady=1) 
       
        rowCount+=1

    updateTable(page)

checkboxesVars=[]
def updateTable(page):
    global checkboxesVars
    page=int(page)
    checkboxesVars.clear()
    for child in frm_table.winfo_children():
        if(type(child)==tk.Label):
            child.destroy()
        elif(type(child)==tk.Checkbutton):
            child.destroy()    
    
    rowCount=1
    for j in range((page-1)*20,page*20):

        lbl_cod=tk.Label(master=frm_table,text=produtos[j]['code'], bg="white")
        lbl_cod.grid(row=rowCount, column=0,sticky='nesw',padx=1,pady=1) 

        lbl_prod=tk.Label(master=frm_table,text=produtos[j]['product'], bg="white")
        lbl_prod.grid(row=rowCount, column=1,sticky='nesw',padx=1,pady=1) 

        lbl_price=tk.Label(master=frm_table,text=produtos[j]['price'], bg="white")
        lbl_price.grid(row=rowCount, column=2,sticky='nesw',padx=1,pady=1)
        prodNumber=rowCount+(20*(currentPage-1))
        checkboxesVars.append(tk.BooleanVar())
        cbx_prod=tk.Checkbutton(master=frm_table,bg="white",onvalue=True, offvalue=False, variable=checkboxesVars[rowCount-1], command=checkCheckboxes)
        cbx_prod.grid(row=rowCount, column=3,sticky='nesw',padx=1,pady=1)
        if(prodNumber > dataLenght):
            cbx_prod.configure(state='disabled')
        rowCount+=1  

def checkCheckboxes():
    global checkboxesVars
    checkeds=0
    for i in range(len(checkboxesVars)):
        cb_var=checkboxesVars[i]
        if(cb_var.get()):
            checkeds+=1
    if(checkeds==0):
        btn_deleteProd["state"]="disable"
        btn_editProd["state"]="disable"
    elif(checkeds==1):
        btn_deleteProd["state"]="normal"
        btn_editProd["state"]="normal"
    elif(checkeds>1):
        btn_deleteProd["state"]="normal"
        btn_editProd["state"]="disable"

def registerNewProduct(event=None):
    global dataRaw,produtos,ent_registerCode,ent_registerPrice,ent_registerProd
    newProduct={}
    codeNewProd=ent_registerCode.get()
    nameNewProd=ent_registerProd.get()
    price=ent_registerPrice.get().replace(',','.')
    if codeNewProd=='' or nameNewProd=='' or price=='':
        tkinter.messagebox.showwarning('Erro','Todos os campos precisam ser preenchidos')
    else:    
        newProduct['product']=nameNewProd
        newProduct['code']=int(codeNewProd)
        if(price==''):
            price=None
        else:
            price=float(price)
        newProduct['price']=price
        dataRaw.append(newProduct)
        writeToJson(dataRaw)
        produtos=readJson()
        setPage(numberPages)
        updatePageLabel()
        ent_registerCode.delete(0,tk.END)
        ent_registerProd.delete(0,tk.END)
        ent_registerPrice.delete(0,tk.END)

def updatePageLabel():
    global lbl_numberOfPages
    lbl_numberOfPages.configure(text='/'+str(numberPages))

def deleteProduct():
    global produtos,currentPage
    deletedElements=0
    for i in range(len(checkboxesVars)):
        cb_var=checkboxesVars[i]
        if(cb_var.get()):
            deleteIndex=20*(currentPage-1)+i-deletedElements
            dataRaw.pop(deleteIndex)
            deletedElements+=1
    writeToJson(dataRaw)
    produtos=readJson()
    if currentPage>numberPages:
        currentPage=numberPages
    updateTable(currentPage)
    updatePageLabel()
    updatePageEntry()      

def openEditWindow():
    global toEdit,productsWindow
    global ent_editCode,ent_editProd,ent_editPrice
    lastChecked=None
    for i in range(len(checkboxesVars)):
        var=checkboxesVars[i]
        if(var.get()):
            lastChecked=i

    toEdit=20*(currentPage-1)+lastChecked
    editWindow=tk.Toplevel(productsWindow)
    editWindow.grab_set()
    editWindow.iconbitmap('icon.ico')
    checkPriceInputCommandEdit=editWindow.register(checkPriceInput)
    frm_editProd=tk.Frame(
        master=editWindow,
        relief=tk.RIDGE,
        borderwidth=2,
    )
    frm_editProd.columnconfigure(0,weight=1,minsize=80)
    frm_editProd.columnconfigure(1,weight=5,minsize=240)
    frm_editProd.columnconfigure(2,weight=1,minsize=40)
    frm_editProd.pack(fill=tk.X,padx=10,pady=10)

    lbl_editTitle=tk.Label(frm_editProd,text="Edite o produto:")
    lbl_editTitle.grid(row=0,column=0,columnspan=3,sticky='nesw')

    lbl_editCode=tk.Label(frm_editProd, text="Código:")
    lbl_editCode.grid(row=1,column=0,sticky='nesw',padx=5,pady=5)
    ent_editCode=tk.Entry(frm_editProd,width=15)
    ent_editCode.grid(row=2,column=0,sticky='nesw',padx=5,pady=5)
    ent_editCode.insert(0,str(produtos[toEdit]['code']))
    ent_editCode.bind('<Return>', editProduct)

    lbl_editProd=tk.Label(frm_editProd, text="Produto:")
    lbl_editProd.grid(row=1,column=1,sticky='nesw',padx=5,pady=5)
    ent_editProd=tk.Entry(frm_editProd)
    ent_editProd.grid(row=2,column=1,sticky='nesw',padx=5,pady=5)
    ent_editProd.insert(0,str(produtos[toEdit]['product']))
    ent_editProd.bind('<Return>', editProduct)

    lbl_editPrice=tk.Label(frm_editProd, text="Preço:")
    lbl_editPrice.grid(row=1,column=2,sticky='nesw',padx=5,pady=5)
    ent_editPrice=tk.Entry(frm_editProd,width=5,validate="key",validatecommand=(checkPriceInputCommandEdit,"%P"))
    ent_editPrice.insert(0,produtos[toEdit]['price'])
    ent_editPrice.grid(row=2,column=2,sticky='nesw',padx=5,pady=5) 
    ent_editPrice.bind('<Return>', editProduct)

    btn_editSave=tk.Button(frm_editProd,text="Salvar",width=20,command=editProduct)
    btn_editSave.grid(row=3,column=1,columnspan=2,padx=5,pady=5,sticky='nes')

    editWindow.mainloop()
    
def editProduct():
    global dataRaw,produtos
    dataRaw[toEdit]={'code': ent_editCode.get(), 'product': ent_editProd.get(), 'price': float(ent_editPrice.get())}
    writeToJson(dataRaw)
    produtos=readJson()
    updateTable(currentPage)

productsWindowOpen=False
def closeProductsWindow():
    global productsWindowOpen,productsDB
    productsWindow.grab_release()
    productsWindow.destroy()
    productsWindowOpen=False
    productsDB=readJson()

def openProductsWindow():
    global produtos,productsWindow,frm_table,checkPriceInput,checkPageInput,lbl_numberOfPages
    global ent_registerCode,ent_registerProd,ent_registerPrice,ent_currentPage
    global btn_editProd,btn_deleteProd,productsWindowOpen,mainWindow,productsWindow

    if(productsWindowOpen):
        return
    productsWindowOpen=True
    produtos=readJson()
    productsWindow = tk.Toplevel(mainWindow)
    productsWindow.grab_set()
    productsWindow.configure(bg='white',padx=10,pady=10)
    productsWindow.minsize(500,650)
    productsWindow.title('Gerenciamento de Produtos')
    productsWindow.iconbitmap('icon.ico')
    productsWindow.protocol("WM_DELETE_WINDOW",closeProductsWindow)
    
    checkPageInputCommand=productsWindow.register(checkPageInput)
    checkPriceInputCommand=productsWindow.register(checkPriceInput)
    codeValidationCommand=productsWindow.register(codeValidation)

    lbl_title=tk.Label(productsWindow,text="Produtos", bg="white",font=("Tahoma", 25))
    lbl_title.pack()

    frm_table = tk.Frame(
        productsWindow,
        bg="black",
        relief=tk.RIDGE,
        borderwidth=2,
        )
    frm_table.columnconfigure(0,weight=2,minsize=100)
    frm_table.columnconfigure(1,weight=10,minsize=200)
    frm_table.columnconfigure(2,weight=1,minsize=60)
    frm_table.columnconfigure(3,weight=1,minsize=50)
    frm_table.pack(fill=tk.X,padx=10,pady=10)
    renderTable(1)

    frm_middle=tk.Frame(productsWindow)
    frm_middle.pack()

    btn_previousPage=tk.Button(frm_middle,text="<",width=2,command=previousPage)
    btn_previousPage.grid(row=0,column=0,padx=3,pady=1)

    ent_currentPage=tk.Entry(frm_middle,width=2,validate="key",validatecommand=(checkPageInputCommand,"%P"))
    ent_currentPage.insert(0,str(currentPage))
    ent_currentPage.bind('<Return>', setPage)
    ent_currentPage.grid(row=0,column=1,padx=3,pady=1)

    lbl_numberOfPages=tk.Label(frm_middle,text='/'+str(numberPages))
    lbl_numberOfPages.grid(row=0,column=2,padx=3,pady=1)

    btn_nextPage=tk.Button(frm_middle,text=">",width=2,command=nextPage)
    btn_nextPage.grid(row=0,column=3,padx=4,pady=1)

    btn_editProd=tk.Button(frm_middle,text="Editar", state="disable", command=openEditWindow)

    btn_editProd.grid(row=0,column=4)

    btn_deleteProd=tk.Button(frm_middle,text="Deletar", state="disable", command=deleteProduct)
    btn_deleteProd.grid(row=0,column=5)

    frm_registerProd=tk.Frame(
        productsWindow,
        relief=tk.RIDGE,
        borderwidth=2,
        )
    frm_registerProd.columnconfigure(0,weight=1,minsize=80)
    frm_registerProd.columnconfigure(1,weight=5,minsize=240)
    frm_registerProd.columnconfigure(2,weight=1,minsize=40)
    frm_registerProd.pack(fill=tk.X,padx=10,pady=10)

    lbl_registerTitle=tk.Label(frm_registerProd,text="Registre um novo produto:")
    lbl_registerTitle.grid(row=0,column=0,columnspan=3,sticky='nesw')

    lbl_registerCode=tk.Label(frm_registerProd, text="Código:")
    lbl_registerCode.grid(row=1,column=0,sticky='nesw',padx=5,pady=5)
    ent_registerCode=tk.Entry(frm_registerProd,width=15,validate='key',validatecommand=(codeValidationCommand,'%P'))
    ent_registerCode.grid(row=2,column=0,sticky='nesw',padx=5,pady=5)
    ent_registerCode.bind('<Return>', registerNewProduct)

    lbl_registerProd=tk.Label(frm_registerProd, text="Produto:")
    lbl_registerProd.grid(row=1,column=1,sticky='nesw',padx=5,pady=5)
    ent_registerProd=tk.Entry(frm_registerProd)
    ent_registerProd.grid(row=2,column=1,sticky='nesw',padx=5,pady=5)
    ent_registerProd.bind('<Return>', registerNewProduct)

    lbl_registerPrice=tk.Label(frm_registerProd, text="Preço:")
    lbl_registerPrice.grid(row=1,column=2,sticky='nesw',padx=5,pady=5)
    ent_registerPrice=tk.Entry(frm_registerProd,width=5,validate="key",validatecommand=(checkPriceInputCommand,"%P"))
    ent_registerPrice.grid(row=2,column=2,sticky='nesw',padx=5,pady=5)
    ent_registerPrice.bind('<Return>', registerNewProduct)

    btn_registerSave=tk.Button(frm_registerProd,text="Cadastrar",width=20,command=registerNewProduct)
    btn_registerSave.grid(row=3,column=1,columnspan=2,padx=5,pady=5,sticky='nes')

    productsWindow.mainloop()
    

productToAdd=False

def findProd(code):
    try:
        code=int(code)
    except:
        if code!='':
            return False
    global productsDB, productToAdd,ent_prodName,ent_unitPrice,ent_totalPrice,ent_quantity
    if code == '':
        productToAdd=False
    else:
        productToAdd=next((item for item in productsDB if item["code"] == code), False)
    if productToAdd:
        ent_prodName.configure(state='normal')
        ent_prodName.delete(0,tk.END)
        ent_unitPrice.configure(state='normal')
        ent_unitPrice.delete(0,tk.END)
        prod=productToAdd['product']
        price=productToAdd['price']
        ent_prodName.insert(0,prod)
        ent_unitPrice.insert(0,str(price))
        ent_prodName.configure(state='disabled')
        ent_unitPrice.configure(state='disabled')
    else:
        ent_prodName.configure(state='normal')
        ent_prodName.delete(0,tk.END)
        ent_prodName.configure(state='disabled')
        ent_unitPrice.configure(state='normal')
        ent_unitPrice.delete(0,tk.END)
        ent_unitPrice.configure(state='disabled')


    multiplyQuantity(ent_quantity.get())
    return True

def multiplyQuantity(quantity):
    global productToAdd,ent_totalPrice
    try:
        quantity=int(quantity)
    except:
        if quantity!='':
            return False

    if productToAdd and quantity!='':
        price=productToAdd['price']
        totalPrice=round(price*quantity,2)
        ent_totalPrice.configure()
        ent_totalPrice.configure(state='normal')
        ent_totalPrice.delete(0,tk.END)
        ent_totalPrice.insert(0,str(totalPrice))
        ent_totalPrice.configure(state='disabled')
    else:
        ent_totalPrice.configure(state='normal')
        ent_totalPrice.delete(0,tk.END)
        ent_totalPrice.configure(state='disabled')
  

    return True

def closeCart():
    global cartList,subTotalStr,subTotalVal,currentProd_var
    result=tkinter.messagebox.askquestion('Confirmação','Você deseja encerrar o atendimento?')
    if result=='yes':
        cartList=[]
        updateCartTable()
        subTotalVal=0
        subTotalStr.set('R$ '+ str(subTotalVal))
        currentProd_var.set('')

def addProd(): 
    global cartPage,ent_code,ent_quantity,productToAdd,ent_prodName,ent_unitPrice,ent_totalPrice,ent_quantity,cartList,subTotalStr,subTotalVal, currentProd_var,numberCartPages
    if productToAdd:
        quantity=ent_quantity.get()
        if quantity!='':
            productToAdd['quantity']=int(quantity)
            totalPrice=round(float(ent_totalPrice.get()),2)
            productToAdd['totalPrice']=totalPrice
            cartList.append(productToAdd.copy())
            currentProd_var.set(str(productToAdd['quantity']) + ' x ' + productToAdd['product'])
            subTotalVal+=totalPrice
            subTotalStr.set('R$ '+ str(round(subTotalVal,2)))
            ent_code.delete(0,tk.END)
            ent_quantity.delete(0,tk.END)
            numberCartPages=math.ceil(len(cartList)/15)
            updateCartPageLabel()
            cartPage=numberCartPages
            updateCartPageEntry()
            updateCartTable()
        else:
            tkinter.messagebox.showwarning("Erro","Você precisa informar uma quantidade")
    else:
        tkinter.messagebox.showwarning("Erro","Você precisa informar um código de produto válido")

cartPage=1
numberCartPages=1
def updateCartTable():
    global cartList,cartPage,cartRows,numberCartPages
    numberCartPages=math.ceil(len(cartList)/15)
    for i in range(15):
        try:
            productIndex=i+((cartPage-1)*15)
            productInRow=cartList[productIndex]
        except:
            productInRow={'code':'','product':'','price':'','quantity':'','totalPrice':''}
        cartRows[i][0].set(productInRow['code'])
        cartRows[i][1].set(productInRow['product'])
        cartRows[i][2].set(productInRow['price'])
        cartRows[i][3].set(productInRow['quantity'])
        cartRows[i][4].set(productInRow['totalPrice'])

def updateCartPageLabel():
    lbl_numberOfCartPages.configure(text='/'+str(numberCartPages))

def nextCartPage():
    global cartPage,numberCartPages
    cartPage=int(cartPage)
    if(cartPage<numberCartPages):
        cartPage+=1
        updateCartPageEntry()

def previousCartPage():
    global cartPage
    cartPage=int(cartPage)
    if(cartPage>1):
        cartPage-=1
        updateCartPageEntry()

def setCartPage(event=None):
    global cartPage,ent_cartPage
    if(type(event)==tk.Event):
        labelValue=ent_cartPage.get()
    else:
        labelValue=numberCartPages
    if(labelValue!=''):
        cartPage=int(labelValue)
    updateCartPageEntry()
    print(cartPage)

def updateCartPageEntry():
    global cartPage,ent_cartPage
    ent_cartPage.delete(0,tk.END)
    ent_cartPage.insert(0,str(cartPage))
    updateCartTable()

def checkCartPageInput(entInput):
    if(entInput==''):
        return True
    try:
        entInput=int(entInput)
        if(entInput>0 and entInput<=numberCartPages):
            return True
        else:
            return False
    except:
        return False
        

def openMainWindow():
    global productsDB, cartList, cartRows, subTotalStr, subTotalVal, currentProd_var,ent_cartPage
    global mainWindow
    cartList=[]
    productsDB=readJson()
    mainWindow=tk.Tk()
    mainWindow.state('zoomed')
    mainWindow.title('ALGON PDV - SISTEMA PARA CAIXA')
    mainWindow.minsize(960,640)
    mainWindow.iconbitmap('icon.ico')

    checkCartPageInputCommand=mainWindow.register(checkCartPageInput)
    findProdCommand=mainWindow.register(findProd)
    multiplyQuantityCommand=mainWindow.register(multiplyQuantity)

    frm_body = tk.Frame(mainWindow)
    frm_body.pack(fill='both',expand=True)

    frm_body.columnconfigure(0,weight=0)
    frm_body.columnconfigure(1,weight=1)
    frm_body.rowconfigure(0,weight=1)

    frm_left = tk.Frame(frm_body)
    frm_left.grid(row=0,column=0,sticky='ns')
    frm_right = tk.Frame(frm_body)
    frm_right.grid(row=0,column=1,sticky='nesw')

    logo=tk.PhotoImage(file='algon.gif')
    cvs_logo= tk.Canvas(frm_left,width=250,height=200)
    cvs_logo.pack()
    cvs_logo.create_image(20,5,anchor=tk.NW,image=logo)

    currentProd_var=tk.StringVar()
    lbl_currentProd = tk.Label(frm_right, textvariable=currentProd_var, bg='blue',fg='white', font=("Tahoma", 35), padx=20, wraplength=800)
    lbl_currentProd.pack(fill='both',padx=10,pady=10)

    frm_insertLabels = tk.Frame(frm_left)
    frm_insertLabels.pack(anchor='center')

    global ent_code,ent_quantity,ent_prodName,ent_unitPrice,ent_totalPrice,lbl_numberOfCartPages

    lbl_code=tk.Label(frm_insertLabels, text='Código de barras:',font=("Tahoma",16), anchor='w')
    lbl_code.pack(padx=10,fill='both')
    ent_code=tk.Entry(frm_insertLabels, width=20, font=("Tahoma",16), justify='right',validate='key',validatecommand=(findProdCommand,"%P"))
    ent_code.pack(padx=10)

    lbl_quantity=tk.Label(frm_insertLabels, text='Quantidade:',font=("Tahoma",16),anchor='w')
    lbl_quantity.pack(padx=10,fill='both')
    ent_quantity=tk.Entry(frm_insertLabels, width=20, font=("Tahoma",16), justify='right',validate='key',validatecommand=(multiplyQuantityCommand,"%P"))
    ent_quantity.pack(padx=10)

    lbl_prodName=tk.Label(frm_insertLabels, text='Produto:',font=("Tahoma",16),anchor='w')
    lbl_prodName.pack(padx=10,fill='both')
    ent_prodName=tk.Entry(frm_insertLabels, state='disabled', width=20, font=("Tahoma",16), justify='right')
    ent_prodName.pack(padx=10)

    lbl_unitPrice=tk.Label(frm_insertLabels, text='Preço Unitário:',font=("Tahoma",16),anchor='w')
    lbl_unitPrice.pack(padx=10,fill='both')
    ent_unitPrice=tk.Entry(frm_insertLabels, state='disabled', width=20, font=("Tahoma",16), justify='right')
    ent_unitPrice.pack(padx=10)

    lbl_totalPrice=tk.Label(frm_insertLabels, text='Preço Total:',font=("Tahoma",16),anchor='w')
    lbl_totalPrice.pack(padx=10,fill='both')
    ent_totalPrice=tk.Entry(frm_insertLabels, state='disabled', width=20, font=("Tahoma",16), justify='right')
    ent_totalPrice.pack(padx=10)

    btn_addProd=tk.Button(frm_insertLabels,command=addProd, text='Adicionar',fg='white', font=("Tahoma",14), bg='green',activebackground='#1a6628',activeforeground='white',width=16)
    btn_addProd.pack(pady=5)

    btn_closeCart=tk.Button(frm_insertLabels,command=closeCart,text='Fechar Compra', fg='white', font=("Tahoma",14),bg='red',activebackground='#aa0000',activeforeground='white',width=16)
    btn_closeCart.pack(pady=5)

    btn_mngProd=tk.Button(frm_left, text='Gerenciar produtos', font=("Tahoma",14),width=16,height=1, command=openProductsWindow)
    btn_mngProd.pack(side='bottom',padx=10,pady=5,)

    frm_cartTable=tk.Frame(frm_right,bg='white')
    frm_cartTable.pack(fill='both',expand=True,padx=10)
    frm_cartTable.columnconfigure(0,weight=2,minsize=40)
    frm_cartTable.columnconfigure(1,weight=2,minsize=40)
    frm_cartTable.columnconfigure(2,weight=1,minsize=40)
    frm_cartTable.columnconfigure(3,weight=0,minsize=40)
    frm_cartTable.columnconfigure(4,weight=1,minsize=40)
    frm_cartTable.columnconfigure(5,weight=0,minsize=40)
    frm_cartTable.columnconfigure(6,weight=1,minsize=40)

    lbl_cartCode=tk.Label(frm_cartTable,text='Código', padx=5,pady=5,bg='white',font=("Tahoma",14,'bold'))
    lbl_cartCode.grid(row=0,column=0)
    lbl_cartProd=tk.Label(frm_cartTable,text='Produto', padx=5,pady=5,bg='white',font=("Tahoma",14,'bold'))
    lbl_cartProd.grid(row=0,column=1)
    lbl_cartUnitPrice=tk.Label(frm_cartTable,text='Valor Unitário', padx=5,pady=5,bg='white',font=("Tahoma",14,'bold'))
    lbl_cartUnitPrice.grid(row=0,column=2)
    lbl_cartQuantity=tk.Label(frm_cartTable,text='Quantidade', padx=5,pady=5,bg='white',font=("Tahoma",14,'bold'))
    lbl_cartQuantity.grid(row=0,column=4)
    lbl_cartTotalPrice=tk.Label(frm_cartTable,text='Total', padx=5,pady=5,bg='white',font=("Tahoma",14,'bold'))
    lbl_cartTotalPrice.grid(row=0,column=6)  
    cartRows=[]
    rowCount=1

    for i in range(15):
        frm_cartTable.rowconfigure(rowCount,weight=1)
        var_cartCode=tk.StringVar()
        lbl_cartCode=tk.Label(frm_cartTable,textvariable=var_cartCode, padx=5,bg='white',font=("Tahoma",12))
        lbl_cartCode.grid(row=rowCount,column=0)

        var_cartProd=tk.StringVar()
        lbl_cartProd=tk.Label(frm_cartTable,textvariable=var_cartProd, padx=5,bg='white',font=("Tahoma",12))
        lbl_cartProd.grid(row=rowCount,column=1)

        var_cartUnitPrice=tk.StringVar()
        lbl_cartUnitPrice=tk.Label(frm_cartTable,textvariable=var_cartUnitPrice, padx=5,bg='white',font=("Tahoma",12))
        lbl_cartUnitPrice.grid(row=rowCount,column=2)

        lbl_cartX=tk.Label(frm_cartTable,text='x', padx=5,bg='white',font=("Tahoma",12))
        lbl_cartX.grid(row=rowCount,column=3)

        var_cartQuantity=tk.StringVar()
        lbl_cartQuantity=tk.Label(frm_cartTable,textvariable=var_cartQuantity, padx=5,bg='white',font=("Tahoma",12))
        lbl_cartQuantity.grid(row=rowCount,column=4)

        lbl_cartEqual=tk.Label(frm_cartTable,text='=', padx=5,bg='white',font=("Tahoma",12))
        lbl_cartEqual.grid(row=rowCount,column=5)

        var_cartTotalPrice=tk.StringVar()
        lbl_cartTotalPrice=tk.Label(frm_cartTable,textvariable=var_cartTotalPrice, padx=5,bg='white',font=("Tahoma",12))
        lbl_cartTotalPrice.grid(row=rowCount,column=6)

        cartRows.append([var_cartCode,var_cartProd,var_cartUnitPrice,var_cartQuantity,var_cartTotalPrice])

        rowCount+=1

    updateCartTable()
    frm_rBottom=tk.Frame(frm_right)
    frm_rBottom.pack(fill='x',padx=10)

    frm_cartPages=tk.Frame(frm_rBottom)
    frm_cartPages.pack(side='left')

    btn_previousCartPage=tk.Button(frm_cartPages,text="<",width=2,command=previousCartPage)
    btn_previousCartPage.grid(row=0,column=0,padx=3,pady=1)

    ent_cartPage=tk.Entry(frm_cartPages,width=2,validate="key",validatecommand=(checkCartPageInputCommand,"%P"))
    ent_cartPage.insert(0,str(cartPage))
    ent_cartPage.bind('<Return>', setCartPage)
    ent_cartPage.grid(row=0,column=1,padx=3,pady=1)

    lbl_numberOfCartPages=tk.Label(frm_cartPages,text='/1')
    lbl_numberOfCartPages.grid(row=0,column=2,padx=3,pady=1)

    btn_nextCartPage=tk.Button(frm_cartPages,text=">",width=2,command=nextCartPage)
    btn_nextCartPage.grid(row=0,column=3,padx=4,pady=1)

    frm_subTotal=tk.Frame(frm_rBottom,bg='red')
    frm_subTotal.pack(side='right',padx=10,pady=10)

    lbl_subTotalTitle=tk.Label(frm_subTotal,text='Subtotal:',font=("Tahoma",16, 'bold'), anchor='w')
    lbl_subTotalTitle.pack(fill='both')
    
    subTotalVal=0
    subTotalStr=tk.StringVar()
    subTotalStr.set('R$ 0,00')
    lbl_subTotal=tk.Label(frm_subTotal, bg='blue', textvariable=subTotalStr, fg='white', font=("Tahoma",22),padx=10,pady=10, width=17, anchor='e')
    lbl_subTotal.pack()

    lbl_credits=tk.Label(frm_rBottom,text='©Levy Barbosa e Gustavo Lopes')
    lbl_credits.pack(side='bottom')
    

    mainWindow.mainloop()


openMainWindow()


