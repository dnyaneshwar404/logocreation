$(document).ready(function() {
    $('#resultDiv').hide();
    $('#errorDiv').hide();
});
function getLogoCharecters() {
    let companyId = document.getElementById('cid').value;
    console.log(companyId)
    let request = {
        "companyId": companyId,
    }
    $.ajax({
        type : "POST",
        dataType: "json",
        data: request,
        url : "/getCompanyLogo",
        success : function(result) {
            console.log(result);
            let companyData = result.data;
            if (result.statusCode=="200") {
                $('#errorDiv').hide();
                $('#resultDiv').show();
                $('.cid').text(companyData.companyId);
                $('.cname').text(companyData.companyName);
                $('.logochars').text(companyData.logoCharacters);
                
            }else{
                $('#resultDiv').hide();
                $('.error').text(result.message);
                $('#errorDiv').show();
            }

        },
        error : function() {
            return false;
        }
    });
}
function hideResultDiv() {
    $('#resultDiv').hide();
}