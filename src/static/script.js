$(document).ready(function() {
    $('#calc-form').on('submit', function(event) {
        event.preventDefault();
        var expression = $('#expression').val();
        $.ajax({
            url: '/calculate',
            method: 'POST',
            data: { expression: expression },
            success: function(response) {
                var resultElement = $('#result');
                if (response.status === "success") {
                    resultElement.text(response.result)
                        .removeClass('result-error')
                        .addClass('result-success');
                } else {
                    resultElement.text('Error: ' + response.result)
                        .removeClass('result-success')
                        .addClass('result-error');
                }
            },
            error: function(xhr, status, error) {
                var errorMessage = xhr.responseJSON ? xhr.responseJSON.result : 'An unknown error occurred.';
                $('#result').text('Error: ' + errorMessage)
                    .removeClass('result-success')
                    .addClass('result-error');
            }
        });
    });
});
