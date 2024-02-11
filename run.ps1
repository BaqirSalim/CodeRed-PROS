# Run npm command in a new terminal
$npmProcess = Start-Process npm -ArgumentList "run dev" -WorkingDirectory "C:\Users\eworo\PROS-FLIGHT-APP\CodeRed-PROS\frontend" -PassThru

# Run flask command in a new terminal
$flaskProcess = Start-Process flask -ArgumentList "--app app run" -WorkingDirectory "C:\Users\eworo\PROS-FLIGHT-APP\CodeRed-PROS\server" -PassThru

# Wait for both processes to complete
$npmProcess.WaitForExit()
$flaskProcess.WaitForExit()