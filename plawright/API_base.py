from playwright.sync_api import Playwright, sync_playwright, Page
Order_data= {"order":[{"fundingSourceId": "1919", "propertyId": "244", "noOfShares": 25}]}

class APIBase:
    def get_token(self,playwright:Playwright):
        api__request_context=playwright.request.new_context(base_url="https://staging-backend.realbricks.com")
        response=api__request_context.post(url="/api/v1/login",
                                           data={"email":"rediff@yopmail.com","password":"Test@123","pin":"0000"},
                                           headers={"Content-Type":"application/json; charset=utf-8"})
        assert response.ok
        print(response.text())
        responseBody=response.json()
        return responseBody["token"]
    def create_order(self,playwright:Playwright):
        Token=self.get_token(playwright)
        API_request_context = playwright.request.new_context(base_url="https://www.staging-fe.realbricks.com")
        response = API_request_context.post(url="/api/v1/orders",
                                            data=Order_data,
                                            headers={"Authorization":Token,
                                                     "Content-Type":"application/json; charset=utf-8"
                                                     })