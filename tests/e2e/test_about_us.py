def test_about_us_status(test_client):
    response = test_client.get('/about') 
    assert response.status_code == 200 #test request if succeeded 

def test_about_us_content(test_client):
    response = test_client.get('/about')
    assert b'What is Course Elector?' in response.data #tests if about page content is shown
    assert b'CourseElector is an online web service made by UNCC students, for UNCC students.' in response.data
    assert b'as well as view detailed information about their classes contributed by their peers' in response.data
