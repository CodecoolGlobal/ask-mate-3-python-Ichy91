#Implement sorting for the question list.
#The question list can be sorted by title, submission time, message, number of views, and number of votes
#You can choose the direction: ascending or descending
#The order is passed as query string parameters, for example /list?order_by=title&order_direction=desc


from flask import Flask, render_template, redirect, request, url_for
import data_handler

questions = data_handler.get_all_user_story()


def sorting(data_list, key):
    data_list.sort(key = lambda i: i[key], reverse=False)
    if key == "vote_number" or key == "view_number":
       data_list.sort(key = lambda i : int(i[key]), reverse=False)


def reverse(data_list, check):
    if check == "desc":
        data_list.reverse()

