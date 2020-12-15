# coding=utf-8
import Kit
from Demo import demo_blue


@demo_blue.route("/", methods=["GET", "POST"])
def service_demo():
    return Kit.common_rsp("Success")
