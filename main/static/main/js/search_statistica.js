var startDate;
var endDate;
var data_dict;
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

$(document).ready(function () {

    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('DD.MM.Y') + ' \u2013 ' + end.format('DD.MM.Y'));
        startDate = start;
        endDate = end;
    }

    $('#reportrange').daterangepicker({
        locale: {
            format: 'DD.MM.YYYY',
            "applyLabel": "Ок",
            "cancelLabel": "Отмена",
            "fromLabel": "От",
            "toLabel": "До",
            "customRangeLabel": "Произвольный",
            "daysOfWeek": [
                "Вс",
                "Пн",
                "Вт",
                "Ср",
                "Чт",
                "Пт",
                "Сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            firstDay: 1
        },
        startDate: start,
        endDate: end,
        ranges: {
            'Сегодня': [moment(), moment()],
            'Вчера': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Последние 7 дней': [moment().subtract(6, 'days'), moment()],
            'Последние 30 дней': [moment().subtract(29, 'days'), moment()],
            'Этот месяц': [moment().startOf('month'), moment().endOf('month')],
            'Прошлый месяц': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

});

const sendSearchData = (start, end) => {
    $.ajax({
        type: 'POST',
        url: '/statistica_search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'startdate': moment(start).format('YYYY-MM-DD'),
            'enddate': moment(end).format('YYYY-MM-DD'),
        },
        success: (data) => {
            if (data.all_notes) {
                $('#show_content').css("visibility", "visible");
                $('#no_content').css("display", "none");
                data_dict = data;
                chart.data.datasets[0].data = [data.promotions, data.punishments, data.withdrawals]
                chart.update();
                chart.render();
                $('#content_row').replaceWith(`<tr class="text-center text-nowrap" id="content_row"><td>${startDate.format('DD.MM.Y')} \u2013 ${endDate.format('DD.MM.Y')}</td><th scope="row">${data.all_notes}</th><td>${data.promotions}</td><td>${data.punishments}</td><td>${data.withdrawals}</td></tr>`);
            }
            else{
                $('#show_content').css("visibility", "hidden");
                $('#no_content').css("display", "block");
            };
        },
        error: () => {

        }
    })
}

const sendDownloadData = (data) => {
    $.ajax({
        type: 'POST',
        url: '/statistica_docxcreate/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'pars_data': JSON.stringify(data),
            'dateInterval': moment(startDate).format('DD.MM.Y') + ' \u2013 ' + moment(endDate).format('DD.MM.Y'),
        },
        dataType: 'binary',
		xhrFields: {
			'responseType': 'blob'
		},
        success: (data, status, xhr) => {
            var blob = new Blob([data], {type: xhr.getResponseHeader('Content-Type')});
			var link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = 'Statistica.docx';
			link.click();
        },
        error: () => {

        }
    })
}

$('#search_btn').click(function(e){
    e.preventDefault();
    sendSearchData(startDate, endDate);
});

$('#download_btn').click(function(e){
    e.preventDefault();
    sendDownloadData(data_dict);
});

const ctx = document.getElementById('myChart');

const data = {
    labels: ['Поощрения', 'Взыскания', 'Снятия взыскания'],
    datasets: [
        {
            data: [1, 1, 1],
            backgroundColor: ['#27AE60', '#CB4335', '#faeee4'],
        }
    ]
};
const config = {
    type: 'doughnut',
    data: data,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                position: 'bottom',
                text: 'Круговая диаграмма записей',
                font: {
                        size: 15
                }
            }
        }
    },
};
var chart = new Chart(ctx, config);

function handleHover(evt, item, legend) {
    legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
        colors[index] = index === item.index || color.length === 9 ? color : color + '4D';
    });
    legend.chart.update();
}

function handleLeave(evt, item, legend) {
    legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
        colors[index] = color.length === 9 ? color.slice(0, -2) : color;
    });
    legend.chart.update();
}
