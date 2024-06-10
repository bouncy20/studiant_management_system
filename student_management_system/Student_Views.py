from django.shortcuts import render,redirect
from app.models import PedagogicalResource, Student_Notification,Student,Student_Feedback,Student_leave, StudentResult
from django.contrib import messages
import matplotlib.pyplot as plt
import io
import urllib, base64



def Home(request):
    return render(request,'Student/home.html')


def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id

        notification = Student_Notification.objects.filter(student_id = student_id)

        context = {
            'notification':notification
        }
        return render(request,'Student/notification.html',context)
    


def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')




def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        "feedback_history":feedback_history
    }
    return render(request,'Student/feedback.html',context)




def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin=request.user.id)
        feedback = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply = ""
        )
        feedback.save()
        return redirect('student_feedback')
    



def STUDENT_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    student_leave_history = Student_leave.objects.filter(student_id = student)

    context = {
        'student_leave_history':student_leave_history,
    }

            
    return render(request,'Student/apply_leave.html',context)






def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')

        leave_message = request.POST.get('leave_message')
        print(leave_date)
        student_id = Student.objects.get(admin = request.user.id)

        student_leave = Student_leave(
            student_id = student_id,
            data = leave_date,
            message = leave_message
        )
        student_leave.save()
        messages.success(request,'Leave Are Successfuly Sent !')
        return redirect('student_leave')
    

def VIEW_RESULT(request):
    mark = None
    student = Student.objects.get(admin = request.user.id)

    result = StudentResult.objects.filter(student_id = student)
    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark

        mark = assignment_mark + exam_mark

    context = {
        'result':result,
        'mark':mark,
    }
    return render (request,'Student/view_result.html',context)





def STUDENT_PERFORMANCE_ANALYSIS(request):
    # Fetch the student based on the logged-in user
    student = Student.objects.get(admin=request.user.id)
    
    # Fetch the student results
    results = StudentResult.objects.filter(student_id=student)
    
    subjects = [result.subject_id.name for result in results]
    assignment_marks = [result.assignment_mark for result in results]
    exam_marks = [result.exam_mark for result in results]
    
    # Create bar chart
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(subjects))
    
    bar1 = ax.bar(index, assignment_marks, bar_width, label='Assignment Marks')
    bar2 = ax.bar([i + bar_width for i in index], exam_marks, bar_width, label='Exam Marks')
    
    ax.set_xlabel('Subjects')
    ax.set_ylabel('Marks')
    ax.set_title('Student Performance')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(subjects)
    ax.legend()
    
    # Save plot to a PNG image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode the PNG image to base64
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    
    context = {
        'graph': graph,
    }
    
    return render(request, 'Student/performance_analysis.html', context)



def student_resource_list(request):
    resources = PedagogicalResource.objects.all()
    return render(request, 'resources/student_resource_list.html', {'resources': resources})

