from locust import HttpUser
from locust import task

loading_test_detail_dict = dict()


def create_loading_test_user(user_detail_dict: dict, **kwargs):
    """
    :param user_detail_dict: detail_dict should be included host http_method test_path
    another_test_setting_dict are optional
    """
    http_method = user_detail_dict.get("request_method", "get")
    request_url = user_detail_dict.get("request_url", "http://localhost")
    another_test_setting_dict = user_detail_dict.get("another_test_setting_dict", None)
    assert_result_dict = user_detail_dict.get("assert_result_dict", None)
    loading_test_detail_dict.update(
        {
            "http_method": http_method,
            "request_url": request_url,
            "another_test_setting_dict": another_test_setting_dict,
            "assert_result_dict": assert_result_dict
        }
    )
    return HttpUserWrapper


class HttpUserWrapper(HttpUser):
    host = ""
    min_wait = 5
    max_wait = 20

    def on_start(self):
        self.http_method_dict = {
            "get": self.client.get,
            "put": self.client.put,
            "delete": self.client.delete,
            "post": self.client.post,
            "head": self.client.head,
            "options": self.client.options,
            "patch": self.client.patch,
        }
        self.loading_test_detail_dict = loading_test_detail_dict
        self.test_client = self.http_method_dict.get(self.loading_test_detail_dict.get("http_method"))

    @task
    def task_with_api_testka(self):
        another_test_setting_dict: dict = self.loading_test_detail_dict.get("another_test_setting_dict")
        assert_result_dict: dict = self.loading_test_detail_dict.get("assert_result_dict")
        if another_test_setting_dict is not None:
            if assert_result_dict is None:
                self.test_client(
                    self.loading_test_detail_dict.get("request_url"),
                    **self.loading_test_detail_dict.get("another_test_setting_dict")
                )
            else:
                with self.test_client(
                        self.loading_test_detail_dict.get("request_url"),
                        **self.loading_test_detail_dict.get("another_test_setting_dict"),
                        catch_response=True
                ) as response:
                    pass
        else:
            if assert_result_dict is None:
                self.test_client(self.loading_test_detail_dict.get("request_url"))
            else:
                with self.test_client(
                        self.loading_test_detail_dict.get("request_url"),
                        **self.loading_test_detail_dict.get("another_test_setting_dict"),
                        catch_response=True
                ) as response:
                    pass
