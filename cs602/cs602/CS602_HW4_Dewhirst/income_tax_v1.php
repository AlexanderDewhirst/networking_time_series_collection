<?php
    function calculateTax($taxableIncome, $taxBracket) {
        $incTax = 0.0;
        $prevVal = 0;

        foreach($taxBracket as $key => $val) {
            if ($key == "none") {
                $incTax += $taxableIncome * $val;
                break;
            }

            $temp = min($key - $prevVal, $taxableIncome);
            $incTax += $temp * $val;
            $taxableIncome -= $temp;
            $prevVal = $key;
            if ($taxableIncome == 0) {
                break;
            }
        }
        return $incTax;
    }

    function incomeTaxSingle($taxableIncome) {
        $taxBracket = array(
            9700 => 0.10,
            39475 => 0.12,
            84200 => 0.22,
            160725 => 0.24,
            204100 => 0.32,
            510300 => 0.35,
            "none" => 0.37
        );

        return calculateTax($taxableIncome, $taxBracket);

    }

    function incomeTaxMarriedJointly($taxableIncome) {
        $taxBracket = array(
            19400 => 0.10,
            78950 => 0.12,
            168400 => 0.22,
            321450 => 0.24,
            408200 => 0.32,
            612350 => 0.35,
            "none" => 0.37
        );

        return calculateTax($taxableIncome, $taxBracket);

    }

    function incomeTaxMarriedSeparately($taxableIncome) {
        $taxBracket = array(
            9700 => 0.10,
            39475 => 0.12,
            84200 => 0.22,
            160725 => 0.24,
            204100 => 0.32,
            510300 => 0.35,
            "none" => 0.37
        );

        return calculateTax($taxableIncome, $taxBracket);

    }

    function incomeTaxHeadOfHousehold($taxableIncome) {
        $taxBracket = array(
            13850 => 0.10,
            52850 => 0.12,
            84200 => 0.22,
            160700 => 0.24,
            204100 => 0.32,
            510300 => 0.35,
            "none" => 0.37
        );

        return calculateTax($taxableIncome, $taxBracket);
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HW4 Part1 - Dewhirst</title>

  <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

  <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <h3>Income Tax Calculator</h3>

        <form class="form-horizontal" method="post">
            <div class="form-group">
                <label class="control-label col-sm-2" for="netIncome">Your Net Income:</label>
                <div class="col-sm-10">
                <input type="number" step="any" name="netIncome" placeholder="Taxable  Income" required autofocus>
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
                $single = incomeTaxSingle($taxableIncome);
                $marriedJointly = incomeTaxMarriedJointly($taxableIncome);
                $marriedSeparately = incomeTaxMarriedSeparately($taxableIncome);
                $headofHousehold = incomeTaxHeadOfHousehold($taxableIncome);

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
    </div>
</body>
</html>
