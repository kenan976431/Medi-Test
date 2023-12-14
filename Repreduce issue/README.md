# Bug recording 
## Fuzz testing bug list
[EGALE](https://github.com/lin-tan/eagle/tree/main/bug-reproduction)

[DocTer](https://docs.google.com/spreadsheets/d/1DgupQBMVpybHtyOhCO0fRb-oJDZbZSbo7H-AG36AE_c/edit?pli=1#gid=1383411354)

[FreeFuzz](https://github.com/ise-uiuc/FreeFuzz/tree/main/data)

## Meta
### The list of bugs
* Presents error type detected by Meta only.
<table class="tg">
<thead>
  <tr>
    <th class="tg-0lax"> Library   </th>
    <th class="tg-0lax">Operator   </th>
    <th class="tg-0lax">Error Type   </th>
    <th class="tg-0lax"> Deivce   </th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax" rowspan="6">Tensorflow1.13.1   </td>
    <td class="tg-0lax" rowspan="3">BatchNormalize   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">IV-UME   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Convlution/BatchNormalize   </td>
    <td class="tg-0lax">IE   </td>
    <td class="tg-0lax">CPU</td>
  </tr>
  <tr>
    <td class="tg-0lax">Tanh   </td>
    <td class="tg-0lax">PE* </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">MaxPool   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="3">Tensorflow2.3.0   </td>
    <td class="tg-0lax">BatchNormalize   </td>
    <td class="tg-0lax">IE-IVE   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Convlution/BatchNormalize   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">MaxPool   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Pytorch1.1.0   </td>
    <td class="tg-0lax">Convlution   </td>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Pytorch1.10.0   </td>
    <td class="tg-0lax">Convlution   </td>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="3">Mindspore1.0.1   <br></td>
    <td class="tg-0lax">MaxPool   </td>
    <td class="tg-0lax">IE-UME</td>
    <td class="tg-0lax">CPU</td>
  </tr>
  <tr>
    <td class="tg-0lax">Sigmoid</td>
    <td class="tg-0lax">IE-UME </td>
    <td class="tg-0lax">CPU</td>
  </tr>
  <tr>
    <td class="tg-0lax">LeakyReLU   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="3">Mindspore1.6.1   </td>
    <td class="tg-0lax">Convlution/BatchNormalize   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">MaxPool   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">Mindspore1.9.0   </td>
    <td class="tg-0lax">Convlution/BatchNormalize   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">MaxPool   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="5">MXnet1.9.1   </td>
    <td class="tg-0lax" rowspan="2">Conv   </td>
    <td class="tg-0lax"> IE-UME</td>
    <td class="tg-0lax"> CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax"> PE*   </td>
    <td class="tg-0lax">  CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">MaxPool   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Sigmoid   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">LeakyReLU   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="6">MNN2.3.0   </td>
    <td class="tg-0lax"> BatchNormalize   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Convlution   </td>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">CPU</td>
  </tr>
  <tr>
    <td class="tg-0lax">Tanh </td>
    <td class="tg-0lax">PE*   </td>
    <td class="tg-0lax">CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">DeepwiseConvlution</td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">PE*</td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
  <tr>
    <td class="tg-0lax">Sigmoid   </td>
    <td class="tg-0lax">IE-UME   </td>
    <td class="tg-0lax">GPU/CPU   </td>
  </tr>
</tbody>
</table>
