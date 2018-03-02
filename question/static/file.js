window.onload = function(){var today = new Date();
        var h = today.getHours();
        var m = today.getMinutes();
        var s = today.getSeconds();
        var month = today.getMonth()+1;
        var year = today.getFullYear();
        var date = today.getDate();
        var day =  today.getDay();
        var _pause = 0;
        spa = document.getElementsByClassName("hid")[0];
        $(document).ready(function(){
            $("#show").show();

    document.getElementById('date').innerHTML =year + "-" + "0" + date + "-" +"0" +month;
    document.getElementById('txt').innerHTML =
      h + ":" + m + ":" + s;

    var t = setTimeout(startTime, 1000);
        });
        function checkTime(i) {
            if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
            return i;
        }
        spa.onclick = function() {
            $("#show").hide();
        }
        window.onclick = function() {
            $("#show").hide();
        }
        function startTime() {
            var flag=0;
            if(s==59)
            {
                s=0;
                flag=1;
            }
            else
            {    s=s+1;

            }
            if(flag==1)
            {
                flag=0;
                if(m==59)
                {
                    m=0;
                    flag=1;
                }
                else{
                    m=m+1;
                }
            }
            if(flag==1)
            {
                flag=0;
                if(h==23)
                {
                    h=0;
                    flag=1;
                }
                else{
                    h=h+1;
                }
            }
            if(flag==1)
            {
                date=date+1;
            }


            document.getElementById('date').innerHTML =year + "-" + "0" +date + "-" + "0" +month;
            document.getElementById('txt').innerHTML =h + ":" + m + ":" + s;
            if(_pause==1)
            {   _pause=0;
                t=setTimeout(startTime,5000);
            }
           else
            var t = setTimeout(startTime, 1000);
        }
        function stopClock() {
             _pause=1;
        }
        }