from datafeed.factor.alpha import AlphaBase


class Alpha158(AlphaBase):

    def get_fields_names(self):
        # ['CORD30', 'STD30', 'CORR5', 'RESI10', 'CORD60', 'STD5', 'LOW0',
        # 'WVMA30', 'RESI5', 'ROC5', 'KSFT', 'STD20', 'RSV5', 'STD60', 'KLEN']
        fields = []
        names = []

        # kbar
        fields += [
            "(close-open)/open",
            "(high-low)/open",
            "(close-open)/(high-low+1e-12)",
            "(high-greater(open, close))/open",
            "(high-greater(open, close))/(high-low+1e-12)",
            "(less(open, close)-low)/open",
            "(less(open, close)-low)/(high-low+1e-12)",
            "(2*close-high-low)/open",
            "(2*close-high-low)/(high-low+1e-12)",
        ]
        names += [
            "KMID",
            "KLEN",
            "KMID2",
            "KUP",
            "KUP2",
            "KLOW",
            "KLOW2",
            "KSFT",
            "KSFT2",
        ]

        # =========== price ==========
        feature = ["OPEN", "HIGH", "LOW", "CLOSE"]
        windows = range(5)
        for field in feature:
            field = field.lower()
            fields += ["shift(%s, %d)/close" % (field, d) if d != 0 else "%s/close" % field for d in windows]
            names += [field.upper() + str(d) for d in windows]

        # ================ volume ===========
        fields += ["shift(volume, %d)/(volume+1e-12)" % d if d != 0 else "volume/(volume+1e-12)" for d in windows]
        names += ["VOLUME" + str(d) for d in windows]

        # ================= rolling ====================

        windows = [5, 10, 20, 30, 60]
        fields += ["shift(close, %d)/close" % d for d in windows]
        names += ["ROC%d" % d for d in windows]

        fields += ["mean(close, %d)/close" % d for d in windows]
        names += ["MA%d" % d for d in windows]

        fields += ["std(close, %d)/close" % d for d in windows]
        names += ["STD%d" % d for d in windows]

        #fields += ["slope(close, %d)/close" % d for d in windows]
        #names += ["BETA%d" % d for d in windows]

        fields += ["ts_max(high, %d)/close" % d for d in windows]
        names += ["MAX%d" % d for d in windows]

        fields += ["ts_min(low, %d)/close" % d for d in windows]
        names += ["MIN%d" % d for d in windows]

        fields += ["quantile(close, %d, 0.8)/close" % d for d in windows]
        names += ["QTLU%d" % d for d in windows]

        fields += ["quantile(close, %d, 0.2)/close" % d for d in windows]
        names += ["QTLD%d" % d for d in windows]

        #fields += ["ts_rank(close, %d)" % d for d in windows]
        #names += ["RANK%d" % d for d in windows]

        fields += ["(close-ts_min(low, %d))/(ts_max(high, %d)-ts_min(low, %d)+1e-12)" % (d, d, d) for d in windows]
        names += ["RSV%d" % d for d in windows]

        fields += ["ts_argmax(high, %d)/%d" % (d, d) for d in windows]
        names += ["IMAX%d" % d for d in windows]

        fields += ["ts_argmin(low, %d)/%d" % (d, d) for d in windows]
        names += ["IMIN%d" % d for d in windows]

        fields += ["(ts_argmax(high, %d)-ts_argmin(low, %d))/%d" % (d, d, d) for d in windows]
        names += ["IMXD%d" % d for d in windows]

        fields += ["correlation(close, log(volume+1), %d)" % d for d in windows]
        names += ["CORR%d" % d for d in windows]

        fields += ["correlation(close/shift(close,1), log(volume/shift(volume, 1)+1), %d)" % d for d in windows]
        names += ["CORD%d" % d for d in windows]

        fields += ["mean(close>shift(close, 1), %d)" % d for d in windows]
        names += ["CNTP%d" % d for d in windows]

        fields += ["mean(close<shift(close, 1), %d)" % d for d in windows]
        names += ["CNTN%d" % d for d in windows]

        fields += ["mean(close>shift(close, 1), %d)-mean(close<shift(close, 1), %d)" % (d, d) for d in windows]
        names += ["CNTD%d" % d for d in windows]

        fields += [
            "sum(greater(close-shift(close, 1), 0), %d)/(sum(abs(close-shift(close, 1)), %d)+1e-12)" % (d, d)
            for d in windows
        ]
        names += ["SUMP%d" % d for d in windows]

        fields += [
            "sum(greater(shift(close, 1)-close, 0), %d)/(sum(abs(close-shift(close, 1)), %d)+1e-12)" % (d, d)
            for d in windows
        ]
        names += ["SUMN%d" % d for d in windows]

        fields += [
            "(sum(greater(close-shift(close, 1), 0), %d)-sum(greater(shift(close, 1)-close, 0), %d))"
            "/(sum(abs(close-shift(close, 1)), %d)+1e-12)" % (d, d, d)
            for d in windows
        ]
        names += ["SUMD%d" % d for d in windows]

        fields += ["mean(volume, %d)/(volume+1e-12)" % d for d in windows]
        names += ["VMA%d" % d for d in windows]

        fields += ["std(volume, %d)/(volume+1e-12)" % d for d in windows]
        names += ["VSTD%d" % d for d in windows]

        fields += [
            "std(abs(close/shift(close, 1)-1)*volume, %d)/(mean(abs(close/shift(close, 1)-1)*volume, %d)+1e-12)"
            % (d, d)
            for d in windows
        ]
        names += ["WVMA%d" % d for d in windows]

        fields += [
            "sum(greater(volume-shift(volume, 1), 0), %d)/(sum(abs(volume-shift(volume, 1)), %d)+1e-12)"
            % (d, d)
            for d in windows
        ]
        names += ["VSUMP%d" % d for d in windows]

        fields += [
            "sum(greater(shift(volume, 1)-volume, 0), %d)/(sum(abs(volume-shift(volume, 1)), %d)+1e-12)"
            % (d, d)
            for d in windows
        ]
        names += ["VSUMN%d" % d for d in windows]

        fields += [
            "(sum(greater(volume-shift(volume, 1), 0), %d)-sum(greater(shift(volume, 1)-volume, 0), %d))"
            "/(sum(abs(volume-shift(volume, 1)), %d)+1e-12)" % (d, d, d)
            for d in windows
        ]
        names += ["VSUMD%d" % d for d in windows]

        return fields, names


if __name__ == "__main__":
    import config

    alpha = Alpha158(config.DATA_DIR)
    alpha.generate_alpha()
    alpha.save_alpha()
    print(alpha.alpha_df.head())
    print(alpha.alpha_df.tail())
    print(alpha.alpha_df.shape)
    print(alpha.alpha_df.columns)
    print(alpha.alpha_df.index)
    print(alpha.alpha_df.describe())
    print(alpha.alpha_df.info())