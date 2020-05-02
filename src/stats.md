---
layout: page
title: Blog stats
---

As of {{ site.time | date: "%-d %B %Y" }}, I've written <strong>{{ site.posts.size }} posts</strong>, which is approximately <strong>{{ site.data["total_word_count"] | divided_by: 1000.0 | round: 1 }}k&nbsp;words</strong>.
You can see how that breaks down over time on the chart below.

You can download the word count data <a href="/word-count.csv">as a CSV</a>.

<script src="/theme/Chart.min.js" type="text/javascript"></script>

<figure class="wide_img">
  <canvas id="wordCount" width="400" height="200"></canvas>
</figure>

<script>
function intComma(value) {
  value = value.toString();
  newValue = value.replace(/^(-?\d+)(\d{3})/, "$1,$2");
  if (newValue === value) {
    return value;
  } else {
    return intComma(newValue);
  }
}

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
        barPercentage: 0.9,
        categoryPercentage: 0.9,
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
        scaleLabel: {
          display: true,
          labelString: "words per month",
          fontSize: 14,
          fontColor: '#202020',
          fontFamily: "Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif",
        },
        ticks: {
          fontSize: 14,
          fontColor: '#202020',
          fontFamily: "Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif",
          beginAtZero: true,
          padding: 8,

          callback: function(value, index, values) {
            return intComma(value);
          }
        }
      }],
      xAxes: [{
        ticks: {
          display: true,
          fontSize: 16,
          padding: 4,
          fontColor: '#202020',
          fontFamily: "Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif",

          /* If you don't set maxTicksLimit, then Chart.js will try to guess
           * where to put ticks, and the January ticks may not appear.
           */
          maxTicksLimit: {{ site.data["per_month_word_count"].size }},          callback: function(value, index, values) {
            month = value.split(" ")[0];
            year = value.split(" ")[1];

            return month == "January" ? year : null;
          }
        },
        gridLines: { display: false }
      }]
    }
  }
});
</script>
