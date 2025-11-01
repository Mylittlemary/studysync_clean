
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import StudySessionForm
from .models import StudySession
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import timedelta, date
from django.http import HttpResponse
from collections import Counter

#toplam süre zaten var :weekly_total
#En çok çalışılan konu 



@login_required
def study_time_chart(request):
    
    form = StudySessionForm()

    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user  # Eğer kullanıcı sistemi varsa
            session.save()

    # Verileri veritabanındaN ÇEK


    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    WEEKLY_GOAL = 300 

    sessions = StudySession.objects.filter(user=request.user, date__range=[seven_days_ago, today]) 

    dates = [s.date.strftime('%d %b') for s in sessions]
    durations =[s.duration for s in sessions]
    weekly_total = sum(durations)


    difficulty = [int(s.difficulty) for s in sessions if s.difficulty]
    mood = [int(s.mood) for s in sessions if s.mood]


    average_duration = sum(durations) / len(durations) if durations else 0
    best_day = dates[durations.index(max(durations))] if durations else "Yok"
    goal_status = "Hedefe ulaşıldı!" if weekly_total >= WEEKLY_GOAL else f"⏳ {WEEKLY_GOAL - weekly_total} dakika kaldı"
    subjects=[s.subject for s in sessions if s.subject]
    #sessions listesindeki her StudySession nesnesinden subject alanını çekmek
    #s.subject oturumun konusu
    #if s.subject boş olmayanları filtrele
    most_common_subject =Counter(subjects).most_common(1)[0][0] if subjects else "Yok"
    #Counter(subjects) her konunun kaç kez geçtiğini sayar.
    #.most_common en sık geçen 1 konuyu döndürür
    #[0][0] sadece konunun adını alır 
    #if subjects else "Yok" eğer hiç konu yoksa Yok yazdır

    #En çok kullanılan kaynak 
    resources =[s.resource for s in sessions if s.resource]
    most_common_resource=Counter(resources).most_common(1)[0][0] if resources else "Yok"

    #Ortalama zorluk ve ruh hali
    average_difficulty = round(sum(difficulty) / len(difficulty), 1) if difficulty else 0
    average_mood = round(sum(mood) / len(mood), 1) if mood else 0


    #Öneri sistemi
    recommendation=""
    
    if most_common_subject !="Yok":
       recommendation+= f"Bu hafta en çok '{most_common_subject}' çalıştın.Haftalık tekrar için 20 dakika ayırabillirisin.\n"

    if average_difficulty >=4 and average_mood <=5:
        recommendation+="Zorluk seviyesi yüksekken modun düşüyor gibi görünüyor.Daha kolay kaynaklarla dengeleyebilirsin.\n"

    if most_common_resource == "Video":
       recommendation += "Video kaynakları sık kullanılmış. Not alarak izlemek verimi artırabilir.\n"

    if average_duration < 30:
       recommendation += "Ortalama çalışma süren kısa. Daha sık ama kısa oturumlar verimli olabilir.\n"

    if recommendation == "":
      recommendation = "Bu hafta dengeli çalışmışsın. Aynı tempoda devam! 💪"






    # Grafik 1
    plt.figure(figsize=(8, 4))
    plt.plot(dates, durations, marker='o', color='teal')  # 👈 EKLE

    plt.xticks(rotation=45)
    plt.title('Günlük Çalışma Süresi')
    plt.xlabel('Tarih')
    plt.ylabel('Dakika')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Grafik 2
    plt.figure(figsize=(6, 4))
    plt.scatter(difficulty, mood, color='purple')
    plt.title('Zorluk Seviyesi vs Ruh Hali')
    plt.xlabel('Zorluk (1-5)')
    plt.ylabel('Ruh Hali (1-10)')
    plt.grid(True)
    plt.tight_layout()
    buffer2 = BytesIO()
    plt.savefig(buffer2, format='png')
    graphic2 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()

    return render(request, 'tracker/dashboard.html', {
        'form': form,
        'chart': graphic, 
        'scatter': graphic2,
        'weekly_average': round(average_duration, 1),

        'best_day': best_day,
        'weekly_goal': WEEKLY_GOAL,
        'weekly_total': weekly_total,
        'goal_status': goal_status,
        'most_common_subject':most_common_subject,
        'most_common_resource' :most_common_resource,
        'average_difficulty':average_difficulty,
        'average_mood':average_mood,
        'recommendation': recommendation,

     


    })
 
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Bağlantı başarılı ")





    