class MortgageCalc:
    # lpr利率
    lpr = 4.3*0.01
    # 基点
    basePoint = -20*0.0001
    # 等额本金月还款列表
    equal_principal_payment_monthly_list = []
    # 等额本息每月还款列表
    equal_loan_payment_monthly_list = []

    def __init__(self, amount, year=30, lpr=4.3*0.01, basePoint=-20*0.0001):
        self.amount = amount
        self.year = year
        self.lpr = lpr
        self.basePoint = basePoint
        #  下面是内部使用的参数
        # 贷款利率
        self.mortgageRate = self.basePoint+self.lpr
        self.totalMonth = self.year*12
        # 每月本金，等额本金贷款需要这个参数
        self.monthlyCapital = self.amount/self.totalMonth
        # 计算每月还款时需要用到的月利率，
        self.monthlyMortgage = self.mortgageRate/12

    def __str__(self) -> str:
        pass
        # 等额本金还贷方式

    def reset(self):
        self.equal_principal_payment_monthly_list = []

    def calc_equal_principal_payment_monthly_list(self):
        # print(f'tm:{self.totalMonth}')
        # 清空数据，重新计算
        self.reset()
        totalInterest = 0
        restCapital = self.amount
        for m in range(0, self.totalMonth):
            currentInterest = restCapital*self.monthlyMortgage
            restCapital -= self.monthlyCapital
            totalInterest += currentInterest
            self.equal_principal_payment_monthly_list.append({
                '本期本金': self.monthlyCapital,
                '本期利息': currentInterest,
                '本期还款': currentInterest+self.monthlyCapital,
                '剩余本金': restCapital,
                '已还本金': self.amount - restCapital,
                '已付利息': totalInterest,
                '已还总额': totalInterest+self.amount-restCapital
            })
        # print(f'每月本金:{"{:0.2f}".format(self.monthlyCapital)}')
        return self.equal_principal_payment_monthly_list

    # 等额本息每月还款计算
    def calc_equal_loan_payment_monthly_list(self):
        # 清空数据，重新计算
        self.equal_loan_payment_monthly_list = []
        # 使用等额本息的公式，可以计算出每月还款的固定数额
        # 等额本息公式只要设置每月还款数额是X,高中数学就能推到出每月还款数额的公式.
        # 每期剩余欠款总金额可以用到等比数列的求和公式,然后我们设置欠款为0,就能算出每月还款金额X的公式
        sumInterestRate = (1+self.monthlyMortgage)**self.totalMonth
        month_payment = self.amount * self.monthlyMortgage * \
            sumInterestRate/(sumInterestRate-1)
        # 剩余本金，用于计算每月偿还利息,初始值就是总的本金
        rest_capital = self.amount
        totalInterest = 0
        for m in range(0, self.totalMonth):
            month_interest = rest_capital*self.monthlyMortgage
            month_capital = month_payment-month_interest
            totalInterest += month_interest
            self.equal_loan_payment_monthly_list.append({
                '本期本金': month_capital,
                '本期利息': month_interest,
                '本期还款': month_payment,
                '剩余本金': rest_capital,
                '已还本金': self.amount - rest_capital,
                '已付利息': totalInterest,
                '已还总额': totalInterest+self.amount-rest_capital
            })
            rest_capital -= month_capital
        return self.equal_loan_payment_monthly_list
        # 等额本金的总还款信息

    @classmethod
    def total_payment(cls, monthly_list):
        infoDict = {
            '总利息': 0,
            '总还款': 0, }
        for monthlyPay in monthly_list:
            infoDict['总还款'] += monthlyPay['本期还款']
        infoDict['总利息'] = infoDict['总还款'] - monthly_list[-1]['已还本金']
        return infoDict

    def elp_info(self):
        self.calc_equal_loan_payment_monthly_list()
        infoDict = {
            '总利息': 0,
            '总还款': 0
        }
        for monthlyPay in self.equal_loan_payment_monthly_list:
            infoDict['总利息'] += monthlyPay['本期利息']
            infoDict['总还款'] += monthlyPay['本期还款']
        return infoDict

    def epp_info(self):
        self.calc_equal_principal_payment_monthly_list()
        infoDict = {
            '总利息': 0,
            '总还款': 0
        }
        for monthlyPay in self.equal_principal_payment_monthly_list:
            infoDict['总利息'] += monthlyPay['本期利息']
            infoDict['总还款'] += monthlyPay['本期还款']
        return infoDict
    # total 是贷款总金额，单位是万
    # mode是还款方式，有等额本金，等额本息
    # year是还款年数
    # lpr是贷款市场报价利率，新的商业住房贷款都是lpr利率。这个每个月20日调整一次，对于还房贷的人来说，每年一月会调整一次.分为一年期和五年期，  单位是1%
    # 其中房贷只用考虑5年期，也就是超过五年的贷款，一年期属于短期贷款
    # 基点，在lpr基础上加上基点就是你的贷款利率，单位是万分之一

    @staticmethod
    def mortgage_month_list(totalCapital, mode='等额本息', year=30, lpr=4.3, basicPoints=-20):
        # 贷款金额
        totalCapitalAmount = totalCapital*10000
        # 贷款利率
        mortgageRate = lpr*0.01 + basicPoints*0.0001
        # 总月数
        totalMonth = year*12
        print(f'贷款利率:{"{:0.2f}%".format(mortgageRate*100)},还款总月数:{totalMonth}')
        if mode == '等额本金':
            monthlyCapital = totalCapitalAmount/totalMonth
            monthRepaymentList = []
            for m in range(0, totalMonth):
                currentInterest = (totalCapitalAmount-m *
                                   monthlyCapital)*mortgageRate/12
                monthRepaymentList.append({
                    '本期本金': monthlyCapital,
                    '本期利息': currentInterest,
                    '本期还款': currentInterest+monthlyCapital
                })
            print(f'每月本金:{"{:0.2f}".format(monthlyCapital)}')
            return monthRepaymentList
        elif mode == '等额本息':
            pass
