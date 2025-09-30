# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)

# 모든 출처(Origin)からの CORS 요청을 허용합니다.
# 실제 운영 환경에서는 특정 도메인으로 제한하는 것이 좋습니다.
CORS(app)

@app.route('/api/random')
def random_number():
    """
    1부터 99 사이의 랜덤한 정수를 생성하고 JSON 형태로 반환합니다.
    """
    number = random.randint(1, 99)
    return jsonify({'number': number})

@app.route('/api/daily_study_check', methods=['GET'])
def daily_study_check():
    """
    사용자의 일별 학습 목표 달성 여부를 시뮬레이션합니다.
    쿼리 파라미터로 'target_hours' (목표 시간)와 'actual_hours' (실제 시간)을 받습니다.
    예: /api/daily_study_check?target_hours=3&actual_hours=2.5
    """
    try:
        # 쿼리 파라미터에서 목표 시간과 실제 시간을 가져옵니다.
        # 기본값을 설정하여 파라미터가 없을 때 오류가 나지 않도록 합니다.
        target_hours = float(request.args.get('target_hours', 0))
        actual_hours = float(request.args.get('actual_hours', 0))

        if target_hours <= 0:
            return jsonify({'error': 'target_hours는 0보다 커야 합니다.'}), 400

        # 목표 달성 여부 로직
        if actual_hours >= target_hours:
            status = "목표 달성!"
            achieved = True
        else:
            status = "목표 미달성. 더 분발해 보세요!"
            achieved = False

        return jsonify({
            'target_hours': target_hours,
            'actual_hours': actual_hours,
            'status': status,
            'achieved': achieved
        })
    except ValueError:
        return jsonify({'error': 'target_hours와 actual_hours는 유효한 숫자여야 합니다.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render.com 환경에서는 Gunicorn이 포트를 관리하므로,
    # 로컬 개발 환경에서만 직접 실행할 때 포트를 지정합니다.
    # Render.com은 'gunicorn app:app' 명령어를 사용합니다.
    app.run(host='0.0.0.0', port=5000)
