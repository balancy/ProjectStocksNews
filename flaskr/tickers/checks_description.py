CHECKS_DESCR = {
    'value': [
        'Is the discounted cash flow value less than 20% of the share price?',
        'Is the discounted cash flow value less than 40% of the share price?',
        'Is the P/E ratio less than the market average but still greater than 0?',
        'Is the P/E ratio less than the industry average but still greater than 0?',
        'Is the PEG ratio within a reasonable range (0 to 1)?',
        'Is the P/B ratio within a reasonable range (0 to 1)?'
    ],

    'health': [
        'Are short term assets greater than short term liabilities?',
        'Are short term assets greater than long term liabilities?',
        'Has the debt to equity ratio increased in the past 5 years?',
        'Is the debt to equity ratio over 40%?',
        'Is debt covered by operating cash flows?',
        'Are earnings greater than 5x the interest on debt (if company pays interest at all)?'
    ],

    'dividends': [
        'Is the current dividend yield higher than the industry average?',
        'Is the current dividend yield higher than the market average?',
        'Is the growth in dividends per share over the past 10 years positive',
        'Has the dividend payed increased in the past 10 years?',
        'Are dividends paid well covered by Net Profit',
        'Is the growth in dividends per share over the past year positive'
    ],

    'past': [
        'Is Has Earnings Per Share (EPS) growth exceeded 20% over the past year?',
        'Is Have Earnings Per Share (EPS) increased in past 5 years?',
        'Is the current EPS growth higher than the average annual growth over the past 5 years?',
        'Is the Return on Equity (ROE) higher than 20%?',
        'Has the Return on Capital Employed (ROCE) increased from 3 years ago?',
        'Is the Return on Assets (ROA) above 5%?'
    ],

    'future': [
        'Is the annual growth rate in earnings expected to exceed the low risk savings rate + inflation?',
        'Is the annual growth rate in earnings expected to exceed the market average in the country of listing?',
        'Is the annual growth rate in revenue expected to exceed the market average in the country of listing?',
        'Is the annual growth rate in earnings above 20%?',
        'Is the annual growth rate in revenue above 20%?',
        'Is the Return on Equity (ROE) in 3 years expected to be over 20%?'
    ]
}
