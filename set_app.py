from flask import Flask,render_template,request,redirect
import set_any_dimension as sad
import card_functions_set as cfs
import web_render_set as wrs
set_app = Flask(__name__)

img_name_dict = {"/static/{}.JPG".format(wrs.cardmapping(card)):wrs.cardmapping(card) for card in sad.get_dimension_list(4)}

@set_app.route('/menu',methods=['GET','POST'])
def whatever():
    if request.method == 'GET':
        return render_template('menupage.html')
    elif request.method == 'POST':
        return redirect('/dimensionpage')


@set_app.route('/dimensionpage',methods=['GET','POST'])
def dimensions():
    if request.method == 'GET':
        return render_template('dimensions.html')
    if request.method == 'POST':
        return redirect('/setpage')


BOARD = sad.board(4)

@set_app.route('/setpage',methods=['GET','POST'])
def setpage():
    
    if request.method == 'GET':
        BOARD.clearboard()
        BOARD.dealcards(12)
        list_sets = ['' for i in range(12)]
        list_cards = ["/static/{}.JPG".format(wrs.cardmapping(card))\
            for card in BOARD.cardsonboard]
        return render_template('setpage.html',l=list_cards,num='',l2=list_sets)
    elif request.method == 'POST':
        list_cards = ["/static/{}.JPG".format(wrs.cardmapping(card))\
            for card in BOARD.cardsonboard]
        num1 = BOARD.numsetsonboard()
        sets = BOARD.printsetsonboard()
        if len(sets) > 0:
            list_sets = ["static/{}.JPG".format(card) for card in sets]
        else:
            list_sets = ['']
        print list_sets
        return render_template('setpage.html',l=list_cards,num=num1,l2=list_sets)








if __name__ == '__main__':
    set_app.run(debug=True)
