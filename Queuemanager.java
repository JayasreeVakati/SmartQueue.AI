// java-backend/QueueManager.java
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Queuemanager {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("📊 SmartQueue.AI - Intelligent Queue Prediction");

        System.out.print("⏰ Enter current hour (24hr): ");
        int hour = scanner.nextInt();

        System.out.print("📆 Enter day of week (0=Mon, 6=Sun): ");
        int day = scanner.nextInt();

        System.out.print("👥 Enter previous hour's customers: ");
        int prev = scanner.nextInt();

        try {
            URL url = new URL("http://127.0.0.1:8000/predict");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json; utf-8");
            con.setDoOutput(true);

            String json = String.format(
                "{\"hour\": %d, \"day_of_week\": %d, \"prev_customers\": %d}",
                hour, day, prev
            );

            try (OutputStream os = con.getOutputStream()) {
                byte[] input = json.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            Scanner responseScanner = new Scanner(con.getInputStream());
            String response = responseScanner.nextLine();
            System.out.println("🔮 Prediction: " + response);

        } catch (Exception e) {
            System.out.println("❌ Error: " + e.getMessage());
        }

        scanner.close();
    }
}
