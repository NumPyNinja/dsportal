from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Course, Module, PracticeQuestions
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import subprocess


def index(request):
    return render(request, 'index.html')


def homepage(request):
    courses = Course.objects.all()
    return render(request, 'home.html', dict(course=courses))


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created.")
            login(request, user)
            messages.info(request, f"You are logged in as {username}")
            return redirect('/home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")
    form = UserCreationForm
    return render(request, 'register.html', context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/home')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in")
                return redirect('/home')
            else:
                messages.error(request, f"Invalid Username and Password")
        else:
            messages.error(request, f"Invalid Username and Password")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def course_detail(request, course_slug):
    if request.user.is_authenticated:
        courses = Course.objects.get(slug=course_slug)
        title = courses.title
        modules = Module.objects.filter(course__title=title)
        return render(request, 'course_list.html', dict(course=courses, module=modules))
    else:
        messages.info(request, f"You are not logged in")
        return redirect('/home')


def module_detail(request, course_slug, module_slug):
    courses = Course.objects.get(slug=course_slug)
    title = courses.title
    modules = Module.objects.filter(course__title=title)
    # practice_questions = PracticeQuestions.objects.filter(course__title=title)
    module_disp = Module.objects.get(slug=module_slug)
    return render(request, 'module_list.html', dict(course=courses, module=modules, module_disp=module_disp))


def practice(request, course_slug):
    courses = Course.objects.get(slug=course_slug)
    title = courses.title
    practice_questions = PracticeQuestions.objects.filter(course__title=title)
    print(practice_questions)
    for q in practice_questions:
        print(q.title)
        print(q.id)
    return render(request, 'questions_display.html', dict(course_title=title, questions=practice_questions))


def questions(request, q_id):
    if request.method == "POST" and request.is_ajax:
        print("post")
        code = request.POST.get("code")
        f = open("ds_code.py", 'w')
        f.write(code)
        f.close()
        test = PracticeQuestions.objects.get(id=q_id)
        print(test.Test)
        f = open("test_sample.py", 'w')
        f.write(test.Test)
        f.close()
        print(test)
        # output = os.system('python ds_code.py')
        try:
            # result = subprocess.run(['python', 'ds_code.py'], capture_output=True, text=True, timeout=3)
            test_result = subprocess.run(['pytest', 'test_sample.py']
                                         , capture_output=True, text=True, timeout=3)
            exit_code = test_result.returncode

            if exit_code == 0:
                message = "Submission Successful"
            elif exit_code == 1:
                message = " Some Tests failed. Please review code"
            elif exit_code == 3:
                message = "Internal error happened while executing tests"
            elif exit_code == 5:
                message = " No tests were collected"
            else:
                message = "Error occurred during submission"
            output = test_result.stdout
            pgm_error = test_result.stderr
            print(output)
            print(pgm_error)
            # return render(request, 'base_iq.html', {'output': output, 'error': pgm_error})
            print(message)
            return JsonResponse({'message': message})
            # return render(request, 'editor.html', {'message': message})
        except:
            print("Code running too long...")
            pgm_error = "Code running too long. Timed out"
            return render(request, 'editor.html', {'error': pgm_error})
    practice_question = PracticeQuestions.objects.get(id=q_id)
    print(practice_question)
    return render(request, 'editor.html', dict(question_to_solve = practice_question))


def tryeditor(request):
    return render(request, 'tryEditor.html')