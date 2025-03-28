

'''
WB17
Tests status code for resources page
'''
def test_status_code(client):
    response = client.get("/activities/resources")
    assert response.status_code == 200


'''
WB18
Tests headers for resources page
'''
def test_headers(client):
    response = client.get("/activities/resources")
    html = response.data.decode("utf-8").replace(" ", "")
    assert '<h1class="roboto-light-500">Cars,Vans,andMotorbikes</h1>' in html
    assert '<h1class="roboto-light-500">Flights</h1>' in html
    assert '<h1class="roboto-light-500">Food</h1>' in html