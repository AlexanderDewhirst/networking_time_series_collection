<?php
  define('TAX_RATES',
    array(
      'Single' => array(
        'Rates' => array(10, 12, 22, 24, 32, 35, 37),
        'Ranges' => array(0, 9700, 39475, 84200, 160725, 204100, 510300),
        'MinTax' => array(0, 970, 4543, 14382, 32748, 46628, 153798)
        ),
      'Married_Jointly' => array(
        'Rates' => array(10, 12, 22, 24, 32, 35, 37),
        'Ranges' => array(0, 19400, 78950, 168400, 321450, 408200, 612350),
        'MinTax' => array(0, 1940, 9086, 28765, 65497, 93257, 164709)
        ),
      'Married_Separately' => array(
        'Rates' => array(10, 12, 22, 24, 32, 35, 37),
        'Ranges' => array(0, 9700, 39475, 84200, 160725, 204100, 306175),
        'MinTax' => array(0, 970, 4543, 14382.50, 32748.50, 46628.50, 82354.75)
        ),
      'Head_Household' => array(
        'Rates' => array(10, 12, 22, 24, 32, 35, 37),
        'Ranges' => array(0, 13850, 52850, 84200, 160700, 204100, 510300),
        'MinTax' => array(0, 1385, 6065, 12962, 31322, 45210, 152380)
        )
      )
  );

  function incomeTax($taxableIncome, $status) {
    $incTax = 0.0;

    $taxBracketData = TAX_RATES[$status];

    foreach(range(0, count($taxBracketData['Ranges']) - 1) as $num) {
      if ($num + 1 > count($taxBracketData['Ranges'])) {
        $incTax += $taxableIncome * $taxBracketData['Rates'][$num];
        break;
      }
      $temp = min($taxableIncome, ($taxBracketData['Ranges'][$num + 1] - $taxBracketData['Ranges'][$num]));
      $incTax += $temp * ($taxBracketData['Rates'][$num] / 100);
      $taxableIncome -= $temp;
      if ($taxableIncome == 0) {
        break;
      }
    }

    return $incTax;
  }
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>HW4 Part2 - Dewhirst</title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
  </head>

  <body>

  <div class="container">
    <h3>Income Tax Calculator</h3>

    <form class="form-horizontal" method="post">
      <div class="form-group">
        <label class="control-label col-sm-2">Enter Net Income:</label>
        <div class="col-sm-10">
          <input type="number"  step="any" name="netIncome" placeholder="Taxable  Income" required autofocus>
        </div>
      </div>
      <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </div>
    </form>

    <?php
      if(isset($_POST['netIncome'])) {
        $taxableIncome = $_POST['netIncome'];
        $single = incomeTax($taxableIncome, "Single");
        $marriedJointly = incomeTax($taxableIncome, "Married_Jointly");
        $marriedSeparately = incomeTax($taxableIncome, "Married_Separately");
        $headofHousehold = incomeTax($taxableIncome, "Head_Household");

        echo "With a net taxable income of $taxableIncome";
        echo "
        <table>
            <thead>
                <tr>
                    <th scope='col'>Status</th>
                    <th scope='col'>Tax</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th scope='row'>Single</th>
                    <td>{$single}</td>
                </tr>
                <tr>
                    <th scope='row'>Married Filing Jointly</th>
                    <td>{$marriedJointly}</td>
                </tr>
                <tr>
                    <th scope='row'>Married Filing Separately</th>
                    <td>{$marriedSeparately}</td>
                </tr>
                <tr>
                    <th scope='row'>Head of Household</th>
                    <td>{$headofHousehold}</td>
                </tr>
            </tbody>
        </table>
        ";
      }

    ?>

    <h3>2019 Tax Tables</h3>

    <?php
      function constructTable($statuses) {
        foreach($statuses as $status) {
          $arrOfIncomes = TAX_RATES[$status]['Ranges'];
          echo $status;
          echo "
          <table>
            <thead>
                <tr>
                    <th scope='col'>Taxable Income</th>
                    <th scope='col'>Tax Rate</th>
                </tr>
            </thead>
            <tbody>
          ";
          foreach(range(1, count($arrOfIncomes)) as $idx) {
            echo "<tr>";
            $taxRate = TAX_RATES[$status]['Rates'][$idx - 1];
            if ($idx == 1) {
              $income = $arrOfIncomes[$idx];
              echo "<th scope='row'>$0 - $$income</th><td>$taxRate%</td>";
            } else if ($idx == count($arrOfIncomes)) {
              $lastIncome = $arrOfIncomes[$idx - 1];
              $incomeTax = incomeTax($lastIncome, $status);
              echo "<th scope='row'>$$lastIncome and over</th><td>$$incomeTax plus $taxRate% of the amount over $$lastIncome</td>";
            } else {
              $lastIncome = $arrOfIncomes[$idx - 1];
              $income = $arrOfIncomes[$idx];
              $incomeTax = incomeTax($lastIncome, $status);
              echo "<th scope='row'>$$lastIncome - $$income</th><td>$$incomeTax plus $taxRate% of the amount over $$lastIncome</td>";
            }
            echo "</tr>";
          }
          echo "
            </tbody>
          </table><br>
          ";
        }
      }

      constructTable(["Single", "Married_Jointly", "Married_Separately", "Head_Household"]);
    ?>
  </div>
</body>
</html>
