var startDate;
var endDate;
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
$(document).ready(function () {

    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('D/MM/Y') + ' \u2013 ' + end.format('D/MM/Y'));
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
        url: '',
        data: {
            'csrfmiddlewaretoken': csrf,
            'startdate': start,
            'enddate': end,
        },
        success: () => {

        },
        error: () => {

        }
    })
}
$('#search_btn').click(function(){
    console.log(startDate.format('D/MM/Y') + ' \u2013 ' + endDate.format('D/MM/Y'));
    sendSearchData(startDate, endDate);
});