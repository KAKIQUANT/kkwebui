from dataclasses import dataclass, field, asdict


@dataclass
class Indicator:
    ind: str = '动量'
    expr: str = 'roc(close,20)'
    name: str = 'roc_20'

@dataclass
class Rule:
    feature_name: str = ''
    ops: str = '>'
    value: float = 0

    def get_expr(self):
        print("try>>",self)
        return self.feature_name+self.ops+str(self.value)

    def parse_from(self, rule: str):
        for op in ['>', '=', '<']:
            if rule.find(op) != -1:
                items = rule.split(op)
                self.feature_name = items[0]
                self.value = float(items[1])
                self.ops = op
                return self





indicators = []
indicators.append(Indicator(ind='动量', expr='roc(close,20)', name='roc_20'))
indicators.append(Indicator(ind='斜率', expr='slope(close,20)', name='slope_20'))
indicators.append(Indicator(ind='RSRS', expr='pair_slope(high,low,18)', name='rsrs_18'))

ind_dict = {ind.ind: ind for ind in indicators}