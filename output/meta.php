<?php
	$xml = simplexml_load_file("data/meta_analyse.xml") 
		or die("Error: Cannot create object");
	$data = array();
	foreach($xml->children() as $child)
	{	
		//echo $child->getName() . ": " . $child . "<br>";
		$data[$child->getName()] = (string)$child;
	}
	//var_dump($data);
	//echo "</br>";
	//echo json_encode($data);
?>
<html>
  <head>
		<title>OryX Statistic Report</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<link href="http://fonts.googleapis.com/css?family=Open+Sans:300,600,700" rel="stylesheet" />
		<script src="js/jquery-1.8.3.min.js"></script>
		<script src="css/5grid/init.js?use=mobile,desktop,1000px"></script>
		<script src="js/jquery.xml2json.js"></script>
		<noscript>
			<link rel="stylesheet" href="css/5grid/core.css" />
			<link rel="stylesheet" href="css/5grid/core-desktop.css" />
			<link rel="stylesheet" href="css/style.css" />
			<link rel="stylesheet" href="css/style-desktop.css" />
		</noscript>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
	<script type="text/javascript">
		var encoded_data = <?php echo json_encode($data) ?>;
	</script>
    <script type="text/javascript">


      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
		var tot = parseInt(encoded_data.pages);
		var des = parseInt(encoded_data.description);
		var key = parseInt(encoded_data.keywords);
		var both = parseInt(encoded_data.both);
		var none = parseInt(encoded_data.none);
		var nometa = tot - des - key;
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
          ['No Meta Data', none],
          ['Meta Description Only', des],
          ['Meta Keywords Only', key],
		  ['Both', both]
        ]);

        // Set chart options
        var options = {'title':'Data from ' + tot + ' Pages',
                       'width':800,
                       'height':600};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
	  
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <!--div id="chart_div"></div>
	<!-- Work -->
			<div class="wrapper wrapper-style2">
			
				<article>
					<header>
						<table class="headertable" style="height:169px">
						<tr>
						<td>
						<span class="image image-centered"><img src="css/images/logo.png" alt="" /></span>
						</td>
						<td style="    text-align: center;">
						<h2>Global Metadata Analysis of Generic Web</h2>
						<span id="count"><strong><?php echo $data['pages']; ?></strong> Page Visits.</span>
						</td>
						</tr>
						</table>
					</header>
					
					<div class="5grid-layout">
						<div class="row">
							<div class="12u">
							<a href="index.html" class="button gbutton-big">Session Statistics</a>
							<a href="global_stats.html" class="button gbutton-big">Global Statistics</a>
							</div>
							
							<div class="8u">
								<section class="box box-style1" style="height: 650px">
									<div>
										<h3>Metadata Analysis</h3>
									</div>
									<div id="chart_div"></div>
								</section>
							</div>
										
						</div>

					</div>
				</article>
				<script type="text/javascript">

		

</script>
			</div>

		<!-- Contact -->
			<div class="wrapper wrapper-style4">
				<article id="contact">
					<footer>
						<p id="copyright">
						&#169; Anghiari.com/Team-OryX - All Rights Reserved 2013 
						</p>
					</footer>
				</article>
			</div>

<script src="js/scripts.js"></script>
	</body>
</html>
  </body>
</html>
