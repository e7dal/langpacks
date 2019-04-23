package com.algorithmia.example;
import com.algorithmia.*;
import java.util.HashMap;

public class Algorithm {
        static String Apply(String input, HashMap<String, String> context) throws Exception{
            if(context.containsKey("local_file")){
                return "hello ".concat(input) + " your model file is downloaded here ".concat(context.get("local_file"));
            }
        return "hello ".concat(input);
    }
    static HashMap<String, String> DownloadModel() throws Exception{
            HashMap<String, String> context = new HashMap<>();
            AlgorithmiaClient client = Algorithmia.client(System.getenv("ALGORITHMIA_API_KEY"));
            String localFile = client.file("data://.my/collection/testfile.json").getFile().getName();
            context.put("local_file", localFile);
            return context;
    }

    public static void main(String[] args) throws Exception {
        AlgorithmHandler algo = new AlgorithmHandler<>(Algorithm::Apply);
        algo.setOnLoad(Algorithm::DownloadModel);
        algo.run();
    }

}