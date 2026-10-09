from fpdf import FPDF

LM = None  # left margin placeholder

class Report(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Stock Market Analysis - SQL Project", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def mc(self, h, text):
        """Wrapper: multi_cell that resets cursor to left margin after."""
        self.set_x(self.l_margin)
        self.multi_cell(0, h, text, new_x="LMARGIN", new_y="NEXT")

    def h1(self, text):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(0, 0, 0)
        self.ln(4)
        self.mc(10, text)
        self.ln(2)

    def h2(self, text):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 60, 120)
        self.ln(3)
        self.mc(8, text)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(20, 20, 20)
        self.mc(5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(20, 20, 20)
        self.mc(5.5, "  - " + text)

    def table(self, headers, rows, widths):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(220, 230, 245)
        for h, w in zip(headers, widths):
            self.cell(w, 8, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for i, row in enumerate(rows):
            self.set_x(self.l_margin)
            fill = (i % 2 == 0)
            self.set_fill_color(248, 250, 252)
            for cell, w in zip(row, widths):
                self.cell(w, 7, str(cell), border=1, fill=fill, align="C")
            self.ln()
        self.ln(3)


pdf = Report(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=15)

# ---------------- PAGE 1: Executive summary ----------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 22)
pdf.set_text_color(30, 60, 120)
pdf.mc(12, "Stock Market Analysis")

pdf.set_font("Helvetica", "", 13)
pdf.set_text_color(90, 90, 90)
pdf.mc(8, "Six NSE Stocks | Jan 2015 - Jul 2018 | SQL Insights")
pdf.ln(6)

pdf.h2("Executive Summary")
pdf.body(
    "This report analyses six NSE-listed stocks over 889 trading days "
    "(January 2015 to July 2018) using SQL. We compute 20-day and 50-day "
    "moving averages, generate golden-cross Buy/Sell signals, and compare "
    "each stock's first and last closing price. "
    "Along the way, we uncover a data trap in plain sight: two stocks "
    "(TCS and Infosys) had 1:1 bonus issues that halved their quoted "
    "prices overnight. Without adjustment, SQL reports these as -24% "
    "and -31% losses - the exact opposite of reality."
)

pdf.h2("Headline Results - Adjusted for Bonus Issues")
pdf.table(
    ["Stock", "Return", "Buys", "Sells", "Latest Signal"],
    [
        ["TVS Motors",    "+86.9%", "8",  "8",  "Sell (2018-05-17)"],
        ["Eicher Motors", "+82.6%", "6",  "7",  "Sell (2018-06-06)"],
        ["TCS *",         "+52.4%", "12", "13", "Sell (2018-06-05)"],
        ["Infosys *",     "+38.2%", "9",  "9",  "Buy  (2018-05-07)"],
        ["Bajaj Auto",    "+10.0%", "12", "11", "Buy  (2018-06-21)"],
        ["Hero Motocorp", "+6.0%",  "9",  "9",  "Sell (2018-05-22)"],
    ],
    widths=[38, 22, 18, 18, 50]
)
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(100, 100, 100)
pdf.mc(4, "* TCS and Infosys raw returns are -23.8% and -30.9% due "
          "to unadjusted bonus issues. See pages 2-3.")
pdf.ln(4)

pdf.h2("Bottom Line")
pdf.bullet("TVS Motors and Eicher Motors were the standout performers (+87%, +83%).")
pdf.bullet("Once adjusted for bonus issues, TCS and Infosys also delivered strong positive returns.")
pdf.bullet("Hero Motocorp was effectively flat over 3.5 years (+6%).")

# ---------------- PAGE 2: Data quality ----------------
pdf.add_page()
pdf.h1("1. Data Quality Issues")

pdf.h2("1.1 Missing values (Task 4)")
pdf.body(
    "Six rows across all six stocks have NULL deliverable_qty. "
    "Critically, these fall on only TWO distinct dates:"
)
pdf.table(
    ["Date", "Stocks affected"],
    [
        ["2015-12-09", "Eicher, Hero, TCS, TVS (4 stocks)"],
        ["2017-08-31", "Bajaj, Infosys (2 stocks)"],
    ],
    widths=[45, 120]
)
pdf.body(
    "Because the gap affects multiple companies on the same day, it is an "
    "exchange-level reporting issue - not a company-specific event. "
    "Our queries using deliverable_qty must be aware of this."
)

pdf.h2("1.2 The data trap - TCS and Infosys bonus issues")
pdf.body(
    "When we rank each stock's single worst trading day (Task 12), two rows "
    "are wildly worse than every other stock:"
)
pdf.table(
    ["Stock", "Worst Day", "Reported Move", "Cause"],
    [
        ["TCS",     "2018-05-31", "-50.2%",        "1:1 bonus issue"],
        ["Infosys", "2015-06-15", "-49.9%",        "1:1 bonus issue"],
        ["Others",  "various",    "-6% to -10%",   "Normal market days"],
    ],
    widths=[35, 40, 45, 45]
)
pdf.body(
    "A large, profitable company cannot lose half its value in one day with "
    "no news. What actually happened: every shareholder received one extra "
    "share for each share they already owned, doubling the total share count. "
    "The price adjusted accordingly - but no investor lost any money."
)

# ---------------- PAGE 3: The Fix and What Changes ----------------
pdf.add_page()
pdf.h1("2. Fixing the Data (Task 13)")

pdf.h2("2.1 Method")
pdf.body(
    "For a 1:1 bonus, divide all prices BEFORE the event date by 2. "
    "Prices on or after the event stay as they are. This produces a "
    "continuous price series that reflects actual investor returns."
)

pdf.h2("2.2 Impact on Returns")
pdf.table(
    ["Stock", "Unadjusted", "Adjusted", "Change"],
    [
        ["TCS",     "-23.8%", "+52.4%", "+76.2pp"],
        ["Infosys", "-30.9%", "+38.2%", "+69.1pp"],
    ],
    widths=[35, 35, 35, 40]
)
pdf.body(
    "Both stocks flip from apparent losers to strong winners. "
    "This is the single most important finding of the project - "
    "the difference between a good investment and a bad one is entirely "
    "due to a data artifact that most ad-hoc analyses would miss."
)

pdf.h2("2.3 Winners vs Losers - Corrected List")
pdf.bullet("Winners: TVS Motors (+87%), Eicher Motors (+83%), TCS (+52%), Infosys (+38%)")
pdf.bullet("Marginal: Bajaj Auto (+10%), Hero Motocorp (+6%)")
pdf.bullet("No stock in the dataset produced a genuine negative return over the period.")

# ---------------- PAGE 4: Method critique + recommendations ----------------
pdf.add_page()
pdf.h1("3. Method Critique & Recommendations")

pdf.h2("3.1 Limitations of the moving-average signal")
pdf.bullet("Moving averages are lagging indicators: they use only past prices, so every Buy/Sell fires after the move has already begun.")
pdf.bullet("Golden-cross strategies generate many false signals in choppy markets - our data shows up to 13 signal flips per stock over 3.5 years.")
pdf.bullet("We did not model transaction costs, brokerage fees, or short-term capital gains tax. These would reduce net returns significantly.")

pdf.h2("3.2 What is missing from the dataset")
pdf.bullet("Dividends - the total return is understated for all six stocks.")
pdf.bullet("Corporate actions beyond bonuses - splits, rights issues, mergers.")
pdf.bullet("Broader market context - Nifty 50 or Sensex would help separate stock-specific performance from market-wide moves.")
pdf.bullet("News and events - earnings surprises, management changes, macro events.")

pdf.h2("3.3 Recommendations")
pdf.bullet("For a real strategy: TCS and Infosys (adjusted) offer the best risk-adjusted entry points.")
pdf.bullet("Any analysis pipeline must include corporate-action adjustment as a first-class step, not an afterthought.")
pdf.bullet("The golden-cross signal works best as a confirmation, not a primary trigger - pair it with fundamentals and volume.")

pdf.ln(6)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(120, 120, 120)
pdf.mc(5,
    "All numbers in this report are reproducible from the SQL file "
    "submitted alongside it, running against the stocks.db database."
)

pdf.output(r"C:\stocks\insights.pdf")
print("PDF written to C:\\stocks\\insights.pdf")