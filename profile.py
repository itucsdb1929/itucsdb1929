from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, jsonify
from statements import delete_message
import db
from functions2 import user_inform

profile = Blueprint('profile', __name__,
                        template_folder='templates')

@profile.route("/api/notifications")
def hasNotifications():
    if session.get('logged_in'):
        cursor = db.get_cursor()
        cursor.execute("select * from Messages where(receiver=%s and has_read=FALSE)", (session['username'],))
        lst = cursor.fetchone()
        if lst:
            return jsonify({'notifications': True})
        else:
            return jsonify({'notifications': False})
    return jsonify({'notifications': False})

@profile.route("/api/delete_message", methods=['POST'])
def deleteMessage():
    message_id = request.form.get('message_id')
    cursor = db.get_cursor()
    connection = db.get_connection()
    delete_message(cursor, message_id)
    connection.commit()
    return jsonify({'result': 'success'})

@profile.route("/api/user_api/<username>", methods=['GET'])
def userApi(username):
    cursor = db.get_cursor()
    connection = db.get_connection()
    res = user_inform(cursor, username)
    connection.commit()
    print("res", res)
    return jsonify(res)

@profile.route("/profile")
def profileFuncMe():
    cursor = db.get_cursor()
    connection = db.get_connection()
    cursor.execute("""update Messages set has_read=TRUE where (receiver=%s)""", (session['username'],))
    connection.commit()
    return redirect(url_for('profile.profileFunc', userName = session['username']))

@profile.route("/profile/<userName>")
def profileFunc(userName):
    session['url'] = url_for('profile.profileFuncMe')
    cursor = db.get_cursor()
    connection = db.get_connection()

    cursor.execute("""select profile_image from users where (username=%s)""", (userName,))
    profileImage = cursor.fetchone()

    cursor.execute("""select friend from friends
                            where (username = %s) """, (userName,))
    friends = cursor.fetchall()
    cursor.execute("""select sender from friendrequests
                            where (friend = %s) """, (userName,))    
    friendRequests = cursor.fetchall()

    me = session['username']

    image_links = ["https://sketchmob.com/wp-content/uploads/2017/09/11189_173340de-347x347.jpg",
                    "https://i.postimg.cc/FRCBcMsT/asada.jpg",
                    "https://i.postimg.cc/kGtfSDH5/original.jpg"]
    message_list = []

    cursor.execute("""select sender, message, message_id from messages where (receiver=%s)""", (userName,))

    message_list = cursor.fetchall()

    return render_template('profile.html', 
                        username = userName,
                        friends = friends,
                        friendRequests = friendRequests, viewer = me, profileImage = profileImage[0],
                            profile_images_len=3, image_links = image_links, message_list = message_list
                        )

@profile.route("/changeProfileImage/<int:imageId>")
def profileImageChange(imageId):
    userName = session['username']
    cursor = db.get_cursor()
    connection = db.get_connection()
    cursor.execute( """update users set profile_image=%s where (username=%s)""", (imageId, userName))
    connection.commit()
    return redirect(url_for('profile.profileFuncMe'))
