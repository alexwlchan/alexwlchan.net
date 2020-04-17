---
layout: page
title: Word count
---

This is an approximate word count for my blog.
To date, I've written about <strong>{{ site.data["total_word_count"] | divided_by: 1000.0 | round: 1 }}k&nbsp;words</strong>.

You can download the word count data <a href="/word-count.csv">as a CSV</a>.

<script src="/theme/Chart.min.js" type="text/javascript"></script>

<figure class="wide_img">
  <canvas id="wordCount" width="400" height="200"></canvas>
</figure>

<script>
var ctx = document.getElementById('wordCount').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [
      {% for row in site.data["per_month_word_count"] %}
        '{{ row[0] }}',
      {% endfor %}
    ],

    datasets: [
      {
        barPercentage: 0.95,
        categoryPercentage: 0.95,
        label: 'Approximate word count',

        data: [
          {% for row in site.data["per_month_word_count"] %}
            {{ row[1] }},
          {% endfor %}
        ],

        backgroundColor: 'rgba(208, 28, 17, 0.7)',
        borderColor: 'rgba(208, 28, 17, 1)',
        borderWidth: 1,
      }
    ]
  },
  options: {
    legend: {
      display: false
    },
    scales: {
      yAxes: [{
        ticks: {
          fontSize: 14,
          fontFamily: "Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif",
          beginAtZero: true
        }
      }],
      xAxes: [{
        ticks: {
          display: true,
          fontSize: 14,
          fontFamily: "Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif",

          /*  I'd like these to display on January, but for some reason only
              every N'th tick mark is displayed. */
          callback: function(value, index, values) {
            console.log(values);
            month = value.split(" ")[0];
            year = value.split(" ")[1];

            return month == "March" ? year : null;
          }
        },
        gridLines: { display: false }
      }]
    }
  }
});
</script>
