﻿using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Text;

// Import namespaces
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.CognitiveServices.Speech.Translation;

namespace speech_translation
{
    class Program
    {
        private static SpeechConfig speechConfig;
        private static SpeechTranslationConfig translationConfig;

        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string cogSvcKey = configuration["CognitiveServiceKey"];
                string cogSvcRegion = configuration["CognitiveServiceRegion"];


                // Configure translation
                translationConfig = SpeechTranslationConfig.FromSubscription(cogSvcKey, cogSvcRegion);
                translationConfig.SpeechRecognitionLanguage = "en-US";
                translationConfig.AddTargetLanguage("fr");
                translationConfig.AddTargetLanguage("es");
                translationConfig.AddTargetLanguage("hi");
                Console.WriteLine("Ready to translate from " + translationConfig.SpeechRecognitionLanguage);

                // Configure speech
                speechConfig = SpeechConfig.FromSubscription(cogSvcKey, cogSvcRegion);

                string targetLanguage = "";
                while (targetLanguage != "quit")
                {
                    Console.WriteLine("\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n");
                    targetLanguage = Console.ReadLine().ToLower();
                    if (translationConfig.TargetLanguages.Contains(targetLanguage))
                    {
                        await Translate(targetLanguage);
                    }
                    else
                    {
                        targetLanguage = "quit";
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task Translate(string targetLanguage)
        {
            string translation = "";
            string phrase = "";

            switch (targetLanguage)
            {
                case "fr":
                    phrase = "Bonjour, je m'appelle Bob et je vais traduire votre phrase";
                    break;
                case "es":
                    phrase = "Hola, mi nombre es Bob y voy a traducir tu frase";
                    break;
                case "hi":
                    phrase = "हैलो, मेरा नाम बॉब है और मैं आपके वाक्यांश का अनुवाद करने जा रहा हूं";
                    break;        
                default:
                    phrase = "I don't understand your phrase - please try again";
                    break;
            }

            // Translate speech
            using AudioConfig audioConfig = AudioConfig.FromDefaultMicrophoneInput();
            using TranslationRecognizer translator = new TranslationRecognizer(translationConfig, audioConfig);
            Console.WriteLine("Speak now...");
            TranslationRecognitionResult result = await translator.RecognizeOnceAsync();
            Console.WriteLine($"{phrase} '{result.Text}'");
            translation = result.Translations[targetLanguage];
            Console.OutputEncoding = Encoding.UTF8;
            Console.WriteLine(translation);

            // Synthesize translation
            var voices = new Dictionary<string, string>
                {
                    ["fr"] = "fr-FR-HenriNeural",
                    ["es"] = "es-ES-ElviraNeural",
                    ["hi"] = "hi-IN-MadhurNeural"
                };
            speechConfig.SpeechSynthesisVoiceName = voices[targetLanguage];
            using SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig);
            SpeechSynthesisResult speak = await speechSynthesizer.SpeakTextAsync(phrase + " " + translation);
            if (speak.Reason != ResultReason.SynthesizingAudioCompleted)
            {
                Console.WriteLine(speak.Reason);
            }

        }

    }
}
