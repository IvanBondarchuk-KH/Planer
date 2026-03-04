from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

events = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_event = {
            'title': request.form.get('title'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'priority': request.form.get('priority')
        }
        if new_event['title']:
            events.append(new_event)
            
        return redirect(url_for('index'))
    
    return render_template('index.html', events=events)

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    if 0 <= event_id < len(events):
        events.pop(event_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)