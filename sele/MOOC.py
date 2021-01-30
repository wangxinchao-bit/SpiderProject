from selenium import webdriver
from time import sleep
import xlwt


class MoocSpider(object):
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(r'../chromedriver.exe')

    def get_content(self):

        self.driver.get(self.url)
        comment_button = self.driver.find_element_by_xpath('//div[@id="review-tag-button"]')
        comment_button.click()
        sleep(2)
        rows = []
        for i in range(1400):
            selectors = self.driver.find_elements_by_xpath('//div[@class="ux-mooc-comment-course-comment_comment-list"]/div')
            for selector in selectors:
                user_name = selector.find_element_by_xpath('.//a[@class="primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name"]').text
                comment_time = selector.find_element_by_xpath('.//div[@class="ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time"]').text
                up_time = selector.find_element_by_xpath('.//span[@class="primary-link"]/span[not(@class)]').text     # 对于没有属性的标签，可以用上述表达式，或者span[@class]
                stars_list = selector.find_elements_by_xpath('.//div[@class="star-point"]/i')
                star_number = len(stars_list)
                comment_text = selector.find_element_by_xpath('.//div[@class="ux-mooc-comment-course-comment_comment-list_item_body_content"]/span').text
                rows.append([user_name, comment_time[4:], up_time, star_number, comment_text])

            next_button = self.driver.find_element_by_xpath('//ul[@class="ux-pager"]/li[@class="ux-pager_btn ux-pager_btn__next"]/a')
            next_button.click()
            sleep(2)
        self.save_data(rows)


    def save_data(self, row_list):
        workbook = xlwt.Workbook(encoding='utf-8')
        comment_sheet = workbook.add_sheet('comment_list', cell_overwrite_ok=True)
        comment_sheet.write(0, 0, '用户姓名')
        comment_sheet.write(0, 1, '评论时间')
        comment_sheet.write(0, 2, '评论点赞人数')
        comment_sheet.write(0, 3, '课程打星')
        comment_sheet.write(0, 4, '评论文本')

        for i in range(len(row_list)):
            for j in range(len(row_list[0])):
                comment_sheet.write(i + 1, j, row_list[i][j])

        workbook.save("comment.xls")



if __name__ == '__main__':
    url = 'https://www.icourse163.org/course/BIT-268001'
    moocspider = MoocSpider(url)
    moocspider.get_content()