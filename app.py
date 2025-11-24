from flask import Flask, request, session, jsonify, render_template, send_from_directory
from scripts import *
import sqlalchemy
import requests
import urllib.request
from flask_login import LoginManager, login_user
from data import db_session
from data.users import Tickets, PlanTime, Ranks, HistoryRanks
from data.db_session import global_init, SqlAlchemyBase
from datetime import datetime, timedelta
from city_support_assistant import rag_classifier, get_client
import promise_analyzer
import bureaucratic_analyzer
import logging
import os
import json



# яндекс ключ к картам  f9727fb1-f338-4780-b4c4-d639d0a62107
#http://localhost:8000/registration?login=user1&name=max&password=1234&password2=12&email=max@gmail.com

#http://localhost:8000/authorization?login=user&password=1234

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# CORS настроен через after_request декоратор ниже

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/base.db')

@login_manager.user_loader
def load_user(user_id):
    # TODO: Добавить модель User если нужна авторизация
    # db_sess = db_session.create_session()
    # return db_sess.query(User).get(user_id)
    return None

db_sess = db_session.create_session()


@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Content-Type: {request.content_type}")
    if request.get_data():
        logger.info(f"Body: {request.get_data()}")




os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger("bot")

level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
try:
    logging.getLogger().setLevel(getattr(logging, level_name, logging.INFO))
    logger.info(f"Log level set to {level_name}")
except Exception:
    logger.info("Log level fallback to INFO")

@app.route("/", methods=["GET"])
def test_server():
    """Главная страница - отображение формы сообщения"""
    try:
        return render_template("message.html")
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return f"Error loading template: {str(e)}", 500


@app.route("/projects", methods=["GET"])
def projects():
    """Страница проектов"""
    try:
        return render_template("projects.html")
    except Exception as e:
        logger.error(f"Error rendering projects template: {str(e)}")
        return f"Error loading template: {str(e)}", 500


@app.route("/messages-list", methods=["GET"])
def messages_list():
    """Страница списка сообщений"""
    try:
        return render_template("messages-list.html")
    except Exception as e:
        logger.error(f"Error rendering messages-list template: {str(e)}")
        return f"Error loading template: {str(e)}", 500


@app.route("/rating", methods=["GET"])
def rating():
    """Страница рейтинга"""
    try:
        return render_template("rating.html")
    except Exception as e:
        logger.error(f"Error rendering rating template: {str(e)}")
        return f"Error loading template: {str(e)}", 500
    

@app.route("/new_ticket",  methods=["POST"])
def new_ticket():
    data = request.get_json() if request.is_json else request.form
    address = data.get("address")
    message = data.get("message")
    topic = data.get("topic")
    email = data.get("email")
    logger.info('New ticket')
    new_tic = Tickets()
    new_tic.address = address
    new_tic.created_at = datetime.now()
    new_tic.status = 'new'
    new_tic.description = message
    db_sess.add(new_tic)
    db_sess.commit()
    print("New tic")
    return {"status": "200"}







@app.route("/ticket_classification", methods=["GET"])
def get_ticket_classification():
    args = request.args
    #user_text = args.get("text")
    rag_classifier(get_client())
    return jsonify({"status": "200"})


@app.after_request
def after_request(response):
    """Добавляет CORS заголовки ко всем ответам"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/getticket")
def get_ticket():
    return jsonify({"status": "200", "result": parse_jsons(get_firts_ticket())})

@app.route("/getclosedticket")
def get_closed_ticket():
    return jsonify({"status": "200", "result": parse_jsons(get_close_tickets())})




@app.route("/queryanalysis", methods=['POST'])
def query_analysis():
    # получаем данные и анализируем 
    try:
        data = request.get_json() if request.is_json else request.form
        
        if data is None:
            data = {}
        
        id = data.get("id")
        text = data.get("text")
        creation_date = data.get("creation_date", "2025-11-22")
        
        if not text:
            return jsonify({"status": "400", "error": "text parameter is required"}), 400
        
        result = promise_analyzer.analyze_promise(text, creation_date)
        logger.info(f"Promise analysis result: {result}")
        
        if result.get("is_promise") == 1:
            if id and result.get("deadline_date"):
                try:
                    planner(result["deadline_date"], id)
                    return jsonify({
                        "status": "200",
                        "result": "add new plan",
                        "analysis": result
                    })
                except Exception as e:
                    logger.error(f"Error in planner: {str(e)}")
                    return jsonify({
                        "status": "200",
                        "result": "analysis completed but plan not created",
                        "error": str(e),
                        "analysis": result
                    })
            else:
                return jsonify({
                    "status": "200",
                    "result": "promise detected but no plan created (missing id or deadline_date)",
                    "analysis": result
                })
        else:
            return jsonify({
                "status": "200",
                "result": "no promise detected",
                "analysis": result
            })
    except Exception as e:
        logger.error(f"Error in query_analysis: {str(e)}")
        return jsonify({"status": "500", "error": str(e)}), 500
    

# @app.route("/datesearch", methods=['GET', 'POST'])
# def date_search():
#     args = request.args
#     text = request.form.get("text")
#     print(text)
#     result = promise_analyzer.analyze_promise(text)
#     planner()
    
#     return result



def planner(data, ticket):
    try:
        plan = PlanTime()
        plan.id_ticket = ticket
        
        # Преобразуем строку даты в datetime объект
        if isinstance(data, str):
            formats = [
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S"
            ]
            
            check_date = None
            for fmt in formats:
                try:
                    check_date = datetime.strptime(data, fmt)
                    break
                except ValueError:
                    continue
            
            if check_date is None:
                logger.error(f"Could not parse date in planner: {data}")
                check_date = datetime.now()
        else:
            check_date = data
        
        plan.check_data = check_date
        plan.end_data = datetime.strptime(
            add_three_days_to_string(check_date.strftime("%Y-%m-%d %H:%M:%S.%f")),
            "%Y-%m-%d %H:%M:%S.%f"
        )
        plan.status = "wait deadline"
        db_sess.add(plan)
        db_sess.commit()
        logger.info(f"Plan created for ticket {ticket} with check_date {check_date}")
    except Exception as e:
        logger.error(f"Error in planner: {str(e)}")
        raise


@app.route("/answerexecutor", methods=["POST"]) # получают из запрсоа какой результат
def answer_executor():
    try:
        answer = request.form.get("answer")
        id_ticket = request.form.get("id")
        
        if not id_ticket:
            return jsonify({"status": "400", "error": "id is required"}), 400
        
        if answer == "closed":
            res = db_sess.query(PlanTime).filter(PlanTime.id_ticket == id_ticket).first()
            if res:
                res.status = "closed"
                db_sess.commit()
                # Обновляем рейтинг (повышаем, так как выполнено добросовестно)
                rank_success = rank(1, id_ticket)
                if rank_success:
                    return jsonify({"status": "200", "result": "plan closed and rank updated"})
                else:
                    return jsonify({"status": "200", "result": "plan closed but rank update failed", "warning": "rank update failed"})
            else:
                return jsonify({"status": "404", "error": "plan not found"}), 404
        else:
            # Обновляем рейтинг (понижаем, так как срок переносится)
            rank_success = rank(0, id_ticket)
            if rank_success:
                return jsonify({"status": "200", "result": "timing extended and rank updated"})
            else:
                return jsonify({"status": "200", "result": "timing extended but rank update failed", "warning": "rank update failed"})
    except Exception as e:
        logger.error(f"Error in answer_executor: {str(e)}")
        return jsonify({"status": "500", "error": str(e)}), 500

    



def push():
    pass



def rank(type, id_ticket):
    """
    Изменяет рейтинг исполнителя в зависимости от результата выполнения заявки
    
    Args:
        type: 0 - понизить рейтинг (перенос срока), 1 - повысить рейтинг (выполнено)
        id_ticket: ID тикета
    """
    try:
        # Получаем тикет
        ticket = db_sess.query(Tickets).filter(Tickets.id == id_ticket).first()
        if not ticket:
            logger.error(f"Ticket with id {id_ticket} not found")
            return False
        
        id_executor = ticket.executor_id
        if not id_executor:
            logger.error(f"Ticket {id_ticket} has no executor_id")
            return False
        
        # Получаем объект рейтинга (не значение, а сам объект!)
        rank_obj = db_sess.query(Ranks).filter(Ranks.id_executor == id_executor).first()
        if not rank_obj:
            logger.error(f"Rank for executor {id_executor} not found")
            return False
        
        # Изменяем значение рейтинга
        if type == 0:  # понижаем рейтинг (перенос срока)
            rank_obj.value -= 10
            change = -10
            notes = f"-10 для исполнителя {id_executor} (тикет {id_ticket})"
        else:  # повышаем рейтинг (выполнено добросовестно)
            rank_obj.value += 10
            change = 10
            notes = f"+10 для исполнителя {id_executor} (тикет {id_ticket})"
        
        # Создаем запись в истории
        history = HistoryRanks()
        history.notes = notes
        db_sess.add(history)
        
        # Сохраняем изменения в базе данных
        db_sess.commit()
        
        logger.info(f"Rank updated for executor {id_executor}: {change} (new value: {rank_obj.value})")
        return True
        
    except Exception as e:
        logger.error(f"Error in rank function: {str(e)}")
        db_sess.rollback()  # Откатываем изменения при ошибке
        return False


@app.route("/count_bureaucratic_responses", methods=["GET", "POST"])
def count_bureaucratic_responses():
    """
    Подсчитывает количество запросов со сложными бюрократическими ответами
    
    GET: возвращает статистику по всем тикетам с resolution
    POST: анализирует переданные тексты ответов
    
    Параметры для POST:
    - texts: список текстов ответов (JSON массив) или
    - text: один текст ответа
    """
    try:
        if request.method == "POST":
            # Анализируем переданные тексты
            data = request.get_json() if request.is_json else request.form
            
            if data is None:
                data = {}
            
            texts = data.get("texts", [])
            text = data.get("text")
            
            # Если передан один текст, преобразуем в список
            if text and not texts:
                texts = [text]
            
            if not texts:
                return jsonify({"status": "400", "error": "texts or text parameter is required"}), 400
            
            # Анализируем ответы
            result = bureaucratic_analyzer.count_bureaucratic_responses(texts)
            
            return jsonify({
                "status": "200",
                "result": {
                    "total": result["total"],
                    "bureaucratic_count": result["bureaucratic_count"],
                    "percentage": result["percentage"],
                    "details": [
                        {
                            "text": texts[i][:100] + "..." if len(texts[i]) > 100 else texts[i],
                            "is_bureaucratic": r["is_bureaucratic"],
                            "confidence": r["confidence"],
                            "complexity_score": r["complexity_score"],
                            "reason": r["reason"]
                        }
                        for i, r in enumerate(result["results"])
                    ]
                }
            })
        else:
            # GET: анализируем все тикеты с resolution из базы данных
            try:
                tickets = db_sess.query(Tickets).filter(Tickets.resolution.isnot(None)).all()
                
                if not tickets:
                    return jsonify({
                        "status": "200",
                        "result": {
                            "total": 0,
                            "bureaucratic_count": 0,
                            "percentage": 0.0,
                            "message": "No tickets with resolution found"
                        }
                    })
                
                # Извлекаем тексты resolution
                resolutions = [ticket.resolution for ticket in tickets if ticket.resolution]
                
                if not resolutions:
                    return jsonify({
                        "status": "200",
                        "result": {
                            "total": 0,
                            "bureaucratic_count": 0,
                            "percentage": 0.0,
                            "message": "No valid resolutions found"
                        }
                    })
                
                # Анализируем ответы
                result = bureaucratic_analyzer.count_bureaucratic_responses(resolutions)
                
                # Получаем детали по каждому тикету
                details = []
                for i, ticket in enumerate(tickets):
                    if ticket.resolution:
                        analysis = bureaucratic_analyzer.is_bureaucratic_response(ticket.resolution)
                        details.append({
                            "ticket_id": ticket.id,
                            "complaint_id": ticket.complaint_id,
                            "resolution_preview": ticket.resolution[:100] + "..." if len(ticket.resolution) > 100 else ticket.resolution,
                            "is_bureaucratic": analysis["is_bureaucratic"],
                            "confidence": analysis["confidence"],
                            "complexity_score": analysis["complexity_score"],
                            "reason": analysis["reason"]
                        })
                
                return jsonify({
                    "status": "200",
                    "result": {
                        "total": result["total"],
                        "bureaucratic_count": result["bureaucratic_count"],
                        "percentage": result["percentage"],
                        "details": details
                    }
                })
            except Exception as e:
                logger.error(f"Error querying database: {str(e)}")
                return jsonify({"status": "500", "error": f"Database error: {str(e)}"}), 500
                
    except Exception as e:
        logger.error(f"Error in count_bureaucratic_responses: {str(e)}")
        return jsonify({"status": "500", "error": str(e)}), 500


@app.route("/analyze_bureaucratic_response", methods=["POST"])
def analyze_bureaucratic_response():
    """
    Анализирует один ответ на предмет бюрократичности
    
    Параметры:
    - text: текст ответа для анализа
    """
    try:
        data = request.get_json() if request.is_json else request.form
        
        if data is None:
            data = {}
        
        text = data.get("text")
        
        if not text:
            return jsonify({"status": "400", "error": "text parameter is required"}), 400
        
        result = bureaucratic_analyzer.is_bureaucratic_response(text)
        
        return jsonify({
            "status": "200",
            "result": result
        })
    except Exception as e:
        logger.error(f"Error in analyze_bureaucratic_response: {str(e)}")
        return jsonify({"status": "500", "error": str(e)}), 500


def add_three_days_to_string(date_str):
    """Добавляет 3 дня к дате в строковом формате"""
    try:
        # Пробуем разные форматы даты
        formats = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S"
        ]
        
        date = None
        for fmt in formats:
            try:
                date = datetime.strptime(str(date_str), fmt)
                break
            except ValueError:
                continue
        
        if date is None:
            logger.error(f"Could not parse date: {date_str}")
            # Возвращаем исходную дату если не удалось распарсить
            return date_str
        
        new_date = date + timedelta(days=3)
        return new_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        logger.error(f"Error in add_three_days_to_string: {str(e)}")
        return date_str







    
if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
    app.debug = True
