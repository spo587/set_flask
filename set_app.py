from flask import Flask,render_template,request,redirect
import set_any_dimension as sad
set_app = Flask(__name__)

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


@set_app.route('/setpage',methods=['GET','POST'])
def setpage():
    if request.method == 'GET':
        board1 = sad.board(4)
        board1.dealcards(12)
        list_cards = ["/static/{}.JPG".format(sad.cardmapping(card))\
         for card in board1.cardsonboard]
        num1 = board1.numsetsonboard()
        return render_template('setpage.html',l=list_cards,num=num1)






if __name__ == '__main__':
    set_app.run(debug=True)