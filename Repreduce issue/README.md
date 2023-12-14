# Bug recording 
## Fuzz testing bug list
[EGALE](https://github.com/lin-tan/eagle/tree/main/bug-reproduction)

[DocTer](https://docs.google.com/spreadsheets/d/1DgupQBMVpybHtyOhCO0fRb-oJDZbZSbo7H-AG36AE_c/edit?pli=1#gid=1383411354)

[FreeFuzz](https://github.com/ise-uiuc/FreeFuzz/tree/main/data)

##  Meta's bug list and its new bugs fixed/confirmed situation
### Meta's bug list
‘*’ Presents error type detected by Meta only.
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

### Meta's new bugs fixed/confirmed situation
'Y' stands for 'YES', 'N' stands for 'NO', '\' stands for have been fixed.
<table class="tg" style="undefined;table-layout: fixed; width: 1097px">
<colgroup>
<col style="width: 171px">
<col style="width: 77px">
<col style="width: 91px">
<col style="width: 520px">
<col style="width: 49px">
<col style="width: 189px">
</colgroup>
<thead>
  <tr>
    <th class="tg-9wq8">DL&nbsp;&nbsp;&nbsp;libray</th>
    <th class="tg-9wq8">operator</th>
    <th class="tg-9wq8">Error Type</th>
    <th class="tg-9wq8">triggering condition</th>
    <th class="tg-9wq8">fixed</th>
    <th class="tg-9wq8">confrmed</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-9wq8" rowspan="2">Tensorflow2.15.0</td>
    <td class="tg-9wq8">BN</td>
    <td class="tg-9wq8">IE-IVE</td>
    <td class="tg-9wq8">set epsilon&lt;0.</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
  <tr>
    <td class="tg-9wq8">BN</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
  <tr>
    <td class="tg-9wq8">Pytorch2.1.1</td>
    <td class="tg-9wq8">Conv</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error.</td>
    <td class="tg-9wq8">N</td>
    <td class="tg-9wq8">N</td>
  </tr>
  <tr>
    <td class="tg-9wq8" rowspan="2">mindspore-gpu1.10.0</td>
    <td class="tg-9wq8" rowspan="2">maxpool</td>
    <td class="tg-9wq8">IE-UME</td>
    <td class="tg-9wq8">Triggering condition is set&nbsp;&nbsp;&nbsp;device to CPU, set dataformat to NHWC.</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
  <tr>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error.</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
  <tr>
    <td class="tg-9wq8" rowspan="5">MNN2.8.0</td>
    <td class="tg-9wq8">BN</td>
    <td class="tg-9wq8">IE-UME</td>
    <td class="tg-9wq8">Triggering condition is set epsilon and momentum.</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
  <tr>
    <td class="tg-9wq8">Conv</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error.</td>
    <td class="tg-9wq8">N</td>
    <td class="tg-9wq8">N</td>
  </tr>
  <tr>
    <td class="tg-9wq8">Tanh</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error</td>
    <td class="tg-9wq8">N</td>
    <td class="tg-9wq8">N</td>
  </tr>
  <tr>
    <td class="tg-9wq8">Tanh</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error</td>
    <td class="tg-9wq8">N</td>
    <td class="tg-ouci"><a href="https://github.com/alibaba/MNN/issues/2241">https://github.com/alibaba/MNN/issues/2241</a></td>
  </tr>
  <tr>
    <td class="tg-9wq8">Dconv</td>
    <td class="tg-9wq8">PE</td>
    <td class="tg-9wq8">Indicating precision error</td>
    <td class="tg-9wq8">Y</td>
    <td class="tg-9wq8">\</td>
  </tr>
</tbody>
</table>
</table>
